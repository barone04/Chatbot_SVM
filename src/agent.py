# src/agent.py
import yaml
from crewai import Agent, Task, Crew, Process
from db_tools import load_llm
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

#============ LOAD LLM ===================
MODEL_NAME="gemini-2.5-flash"
GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")


@CrewBase
class SQLDeveloperCrew():
    """SQLDeveloperCrew"""
    def __init__(self):
        with open("config/agents.yaml", "r") as f:
            self.agents_config = yaml.safe_load(f)
        with open("config/tasks.yaml", "r") as f:
            self.tasks_config = yaml.safe_load(f)

        self.llm = load_llm(MODEL_NAME)

#============== AGENTS =====================
    @agent
    def sql_dev(self) -> Agent:
        cfg = self.agents_config['sql_dev']
        return Agent(
            role=cfg["role"],
            goal=cfg["goal"],
            backstory=cfg["backstory"],
            llm=self.llm,
            tools=[SerperDevTool()],
            allow_delegation=False,
        )

    @agent
    def data_analyst(self) -> Agent:
        cfg = self.agents_config['data_analyst']
        return Agent(
            role=cfg["role"],
            goal=cfg["goal"],
            backstory=cfg["backstory"],
            llm=self.llm,
            allow_delegation=False,
        )

    @agent
    def report_writer(self) -> Agent:
        cfg = self.agents_config['report_writer']
        return Agent(
            role=cfg["role"],
            goal=cfg["goal"],
            backstory=cfg["backstory"],
            llm=self.llm,
            allow_delegation=False,
        )

#==================== TASKS ======================
    @task
    def extract_data(self) -> Task:
        task_cfg = self.tasks_config["extract_data"]
        return Task(
            description=task_cfg["description"],
            expected_output=task_cfg["expected_output"],
            agent=task_cfg["agent"],
        )

    @task
    def analyze_data(self) -> Task:
        task_cfg = self.tasks_config["analyze_data"]
        return Task(
            description=task_cfg["description"],
            expected_output=task_cfg["expected_output"],
            agent=task_cfg["agent"],
            context=task_cfg["context"],
        )

    @task
    def write_report(self) -> Task:
        task_cfg = self.tasks_config["analyze_data"]
        return Task(
            description=task_cfg["description"],
            expected_output=task_cfg["expected_output"],
            agent=task_cfg["agent"],
            context=task_cfg["context"],
        )

#==================== CREW ==========================
    @crew
    def crew(self) -> Crew:
        """Creates the SQLDeveloperCrew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
