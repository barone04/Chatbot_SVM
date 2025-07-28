import os

from crewai import LLM


from dotenv import load_dotenv
load_dotenv()
GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")

llm = LLM(
    model="gemini/gemini-2.0-flash",
    temperature=0.1,
    API_KEY=GOOGLE_API_KEY,
)
llm.call("Who invented transcendental meditation.")

