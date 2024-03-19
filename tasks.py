from textwrap import dedent
from crewai import Task

class Task:
    def research_faults(self, agent, equipment_or_system):
        return Task(
            description=dedent(f"""
                We are looking for possible faults in {equipment_or_system}.
                List as many as you can think of.
                Also, can you return the data in a JSON format. That is a list of fault objects with the properties title and description.
            """),
            expected_output()
        )