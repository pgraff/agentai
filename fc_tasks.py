from crewai import Task, Agent
from fc_model import System, Fault, Faults, Cause, Causes, FaultCauseResult, MergedCausesResult
from textwrap import dedent
import pandas as pd
class Tasks:

    @classmethod
    def identify_faults(cls, agent: Agent, system: System):
        return Task(
            description=f'Identify all possible faults of {system.title} ({system.description}).',
            agent=agent,
            output_pydantic=Faults,
            expected_output=dedent(
                f"""
                I want a complete list of faults in a simple list (no hierarchy).
                """)
            )

    @classmethod
    def identify_causes_for_a_fault(cls, agent, system: System, fault: Fault):
        return Task(
            description=dedent(
                f"""We have identified the fault {fault.title} ({fault.description}) 
                related to {system.title} ({system.title}). 
                Investigate potential causes for {fault.title}
                """),
            agent=agent,
            expected_output="An exhaustive list of causes",
            output_pydantic=Causes
        )

    @classmethod
    def merge_causes(cls, agent, cause_df):
        return Task(
            description = dedent(
            f"""
            I want to discover the duplicates in this set of causes based on the name and description.
            I will givve you a list of the identified causes where each cause is numbered.
            The format will be as follows:
            (id,title,description)
            I want you to find the duplicates and return it to me as.
            ([id1],[id2],merged_title,merged_descriptiption).
            For example, I give you a list as this:
            (1,"No oil","The engine is out of oil")
            (2,"Oil mssing","We don't have any oil")
            ...
            You may recognize that 1 and 2 are describing the same causes and return them as:
            ([1,2],"Missing oil", "The engine is missing oil")
            """),
            agent=agent,
            expected_output="A list of the merged causes",
            output_pydantic=MergedCausesResult
        )
