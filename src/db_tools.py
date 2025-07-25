import json
import os
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List
from crewai.tools import tool
from langchain.schema.output import LLMResult
from langchain_community.tools.sql_database.tool import (
    InfoSQLDatabaseTool,
    ListSQLDatabaseTool,
    QuerySQLCheckerTool,
    QuerySQLDataBaseTool,
)
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_core.callbacks.base import BaseCallbackHandler
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

#============ LOAD LLM ===================
MODEL_NAME="gemini-2.5-flash"
GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")

@dataclass
class Event:
    event: str
    timestamp: str
    text: str


def _current_time() -> str:
    return datetime.now(timezone.utc).isoformat()


class LLMCallbackHandler(BaseCallbackHandler):
    def __init__(self, log_path: Path):
        self.log_path = log_path

    def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> Any:
        """Run when LLM starts running."""
        assert len(prompts) == 1
        event = Event(event="llm_start", timestamp=_current_time(), text=prompts[0])
        with self.log_path.open("a", encoding="utf-8") as file:
            file.write(json.dumps(asdict(event)) + "\n")

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> Any:
        """Run when LLM ends running."""
        generation = response.generations[-1][-1].message.content
        event = Event(event="llm_end", timestamp=_current_time(), text=generation)
        with self.log_path.open("a", encoding="utf-8") as file:
            file.write(json.dumps(asdict(event)) + "\n")



def load_llm(model_name):
    if GOOGLE_API_KEY is None:
        raise ValueError("GOOGLE_API_KEY haven't already created in environment.")

    llm = ChatGoogleGenerativeAI(
        model=model_name,
        google_api_key=GOOGLE_API_KEY,
        temperature=0.5,
        callbacks=[LLMCallbackHandler(Path("prompts.jsonl"))],
    )
    return llm


# Tải database
db_path = os.path.abspath("../data/sales.db")
db_uri = f"sqlite:///{db_path}"
db = SQLDatabase.from_uri(db_uri)
print("Kết nối database thành công!")

@tool("list_tables")
def list_tables() -> str:
    """Danh sách các bảng có trong datasets"""
    return ListSQLDatabaseTool(db=db).invoke("")

@tool("tables_schema")
def tables_schema(tables: str) -> str:
    """
    Đầu vào là danh sách các bảng được phân tách bằng dấu phẩy, đầu ra là lược đồ và các hàng mẫu
    cho các bảng đó. Hãy đảm bảo rằng các bảng thực sự tồn tại bằng cách gọi `list_tables` trước!
    Ví dụ: Đầu vào: table1, table2, table3
    """
    tool1 = InfoSQLDatabaseTool(db=db)
    return tool1.invoke(tables)

@tool("execute_sql")
def execute_sql(sql_query: str) -> str:
    """Thực hiện truy vấn SQL trên cơ sở dữ liệu. Trả về kết quả"""
    return QuerySQLDataBaseTool(db=db).invoke(sql_query)

@tool("check_sql")
def check_sql(sql_query: str) -> str:
    """
    Use this tool to double check if your query is correct before executing it. Always use this
    tool before executing a query with `execute_sql`.
    """
    llm = load_llm(MODEL_NAME)
    return QuerySQLCheckerTool(db=db, llm=llm).invoke({"query": sql_query})
print(check_sql.run("select* WHErE price > 10000 LimIT 5 table = slot"))

# from langchain_core.tools import Tool  # hoặc từ langchain.tools nếu bạn đang dùng phiên bản cũ hơn
#
# list_tables_tool = Tool.from_function(
#     name="list_tables",
#     description="Danh sách các bảng có trong datasets",
#     func=lambda: ListSQLDatabaseTool(db=db).invoke("")
# )
#
# tables_schema_tool = Tool.from_function(
#     name="tables_schema",
#     description="""
#     Đầu vào là danh sách các bảng được phân tách bằng dấu phẩy, đầu ra là lược đồ và các hàng mẫu
#     cho các bảng đó. Hãy đảm bảo rằng các bảng thực sự tồn tại bằng cách gọi `list_tables` trước!
#     Ví dụ: table1, table2, table3
#     """,
#     func=lambda tables: InfoSQLDatabaseTool(db=db).invoke(tables)
# )
#
# execute_sql_tool = Tool.from_function(
#     name="execute_sql",
#     description="Thực hiện truy vấn SQL trên cơ sở dữ liệu. Trả về kết quả",
#     func=lambda sql_query: QuerySQLDataBaseTool(db=db).invoke(sql_query)
# )
#
# check_sql_tool = Tool.from_function(
#     name="check_sql",
#     description="""
#     Use this tool to double check if your query is correct before executing it. Always use this
#     tool before executing a query with `execute_sql`.
#     """,
#     func=lambda sql_query: QuerySQLCheckerTool(db=db, llm=load_llm(MODEL_NAME)).invoke({"query": sql_query})
# )
