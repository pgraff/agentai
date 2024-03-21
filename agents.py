from crewai import Agent
from crewai_tools.tools import WebsiteSearchTool, SerperDevTool, FileReadTool

web_search_tool = WebsiteSearchTool()
serper_dev_tool = SerperDevTool()

class Agents:
    def fault_finder_agent(self, system_or_equipment):
        return Agent(
            role=f"Domain Expert on Faults in {system_or_equipment}",
            goal=f"Suggest possible faults for {system_or_equipment}",
            tools=[web_search_tool, serper_dev_tool],
            backstory=f"Expert in analyzing {system_or_equipment} and to produce a list of likely failures",
            verbose=True
        )

    def cause_finder_agent(self, system_or_equipment, fault_title, fault_description):
        return Agent(
            role=f"Domain Expert on Causes of faults for {system_or_equipment}",
            goal=f"Suggest possible causes for the fault {fault_title} in {system_or_equipment}",
            tools=[web_search_tool, serper_dev_tool],
            backstory=f"We have identified that the fault {fault_title} can occur in {system_or_equipment}. Now we want to know what could cause that",
            verbose=True
        )
