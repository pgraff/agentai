from crewai import Agent
from langchain.tools import DuckDuckGoSearchRun


class RetrieveCandidatesForInvestigation(Agent):
    def __init(self, llm, what_we_are_investigating: str, include_web_search: bool):
        self.role = "Senior Researcher"
        self.goal = f"Suggest candidates for further research that other agents will investigate",
        self.backstory = f"You are responsible for providing a set of candidate topics for others to investigate",
        self.for
        self.verbose = True
        tools = []
        if include_web_search:
            tools.append(DuckDuckGoSearchRun())
        self.tools = tools
