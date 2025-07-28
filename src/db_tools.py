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
from crewai.tools import BaseTool
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_core.callbacks.base import BaseCallbackHandler
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.language_models import BaseLanguageModel
from crewai import LLM
import litellm
from dotenv import load_dotenv, find_dotenv
load_dotenv()
load_dotenv(find_dotenv())

#============ LOAD LLM ===================
MODEL_NAME="gemini/gemini-2.0-flash"
litellm.api_key = os.getenv("GOOGLE_API_KEY")
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


def load_llm():
    llm = LLM(
        model=MODEL_NAME,
        temperature=0.1
    )
    return llm

def load_llm_tools(model_name):
    if GOOGLE_API_KEY is None:
        raise ValueError("GOOGLE_API_KEY haven't already created in environment.")

    llm_tools = ChatGoogleGenerativeAI(
        model=model_name,
        google_api_key=GOOGLE_API_KEY,
        temperature=0.5,
        callbacks=[LLMCallbackHandler(Path("prompts.jsonl"))],
    )
    return llm_tools


# Tải database
db_path = os.path.abspath("../data/sales.db")
db_uri = f"sqlite:///{db_path}"
db = SQLDatabase.from_uri(db_uri)
print("Kết nối database thành công!")


class ListTablesTool(BaseTool):
    name: str = "list_tables"
    description: str = "Danh sách các bảng có trong datasets"

    def _run(self) -> str:
        return ListSQLDatabaseTool(db=db).invoke("")

class TablesSchemaTool(BaseTool):
    name: str = "tables_schema"
    description: str = (
        "Đầu vào là danh sách các bảng được phân tách bằng dấu phẩy, đầu ra là lược đồ và các hàng mẫu "
        "cho các bảng đó. Hãy đảm bảo rằng các bảng thực sự tồn tại bằng cách gọi `list_tables` trước!"
    )

    def _run(self, tables: str) -> str:
        return InfoSQLDatabaseTool(db=db).invoke(tables)

class ExecuteSQLTool(BaseTool):
    name: str = "execute_sql"
    description: str = "Thực hiện truy vấn SQL trên cơ sở dữ liệu. Trả về kết quả"

    def _run(self, sql_query: str) -> str:
        return QuerySQLDataBaseTool(db=db).invoke(sql_query)

class CheckSQLTool(BaseTool):
    name: str = "check_sql"
    description: str = (
        "Sử dụng công cụ này để kiểm tra xem truy vấn của bạn có chính xác hay không trước khi thực thi. "
        "Luôn sử dụng công cụ này trước khi thực thi truy vấn với `execute_sql`."
    )

    def _run(self, sql_query: str) -> str:
        llm = load_llm_tools("gemini-2.0-flash")
        return QuerySQLCheckerTool(db=db, llm=llm).invoke({"query": sql_query})


# list_tool = ListTablesTool()
# print(list_tool.run())
#
# schema_tool = TablesSchemaTool()
# print(schema_tool.run("orders, customers"))
#
# exec_tool = ExecuteSQLTool()
# print(exec_tool.run("SELECT * FROM slot WHErE price > 10000 LIMIT 5"))
#
# check_tool = CheckSQLTool()
# print(check_tool.run("SELECT * FROM slot WhERE price > 10000 LIMIT 5"))





# @tool("list_tables")
# def list_tables() -> str:
#     """Danh sách các bảng có trong datasets"""
#     return ListSQLDatabaseTool(db=db).invoke("")
#
# @tool("tables_schema")
# def tables_schema(tables: str) -> str:
#     """
#     Đầu vào là danh sách các bảng được phân tách bằng dấu phẩy, đầu ra là lược đồ và các hàng mẫu
#     cho các bảng đó. Hãy đảm bảo rằng các bảng thực sự tồn tại bằng cách gọi `list_tables` trước!
#     Ví dụ: Đầu vào: table1, table2, table3
#     """
#     tool1 = InfoSQLDatabaseTool(db=db)
#     return tool1.invoke(tables)
#
# @tool("execute_sql")
# def execute_sql(sql_query: str) -> str:
#     """Thực hiện truy vấn SQL trên cơ sở dữ liệu. Trả về kết quả"""
#     return QuerySQLDataBaseTool(db=db).invoke(sql_query)
#
# @tool("check_sql")
# def check_sql(sql_query: str) -> str:
#     """
#     Sử dụng công cụ này để kiểm tra xem truy vấn của bạn có chính xác hay không trước khi thực thi.
#     Luôn sử dụng công cụ này trước khi thực thi truy vấn với `execute_sql`.
#     """
#     llm = load_llm_tools("gemini-2.0-flash")
#     return QuerySQLCheckerTool(db=db, llm=llm).invoke({"query": sql_query})
# print(check_sql.run("select* WHErE price > 10000 LimIT 5 table = slot"))



