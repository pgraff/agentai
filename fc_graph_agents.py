from typing import List
from crewai import Agent
from textwrap import dedent


from fc_model import System, Cause, Fault, Indicator, Sensor

from langchain_community.llms import Ollama
from langchain import OpenAI

llm_model = Ollama(model="openchat", temperature=0.0)
# from langchain_openai import ChatOpenAI
# llm_model=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.0)

class Agents:

    @classmethod
    def fault_researcher(cls, system: System, verbose: bool = False):
        if system.goals is not None and len(system.goals) > 1:
            goal = system.goals
        else:
            goal = f"Find all known faults related to {system.title}"
        return Agent(
            role=f"Senior researcher that is an expert on {system.title}",
            goal=goal,
            backstory=dedent(
                f"""We are building a fault-cause graph for {system.title}, 
                but we are only resposible for finding the faults
                """),
            llm=llm_model,
            max_iter=10,
            verbose=verbose)

    @classmethod
    def cause_researcher(cls, system: System, fault: Fault, verbose: bool = False):
        return Agent(
            role=f"Senior researcher that is an expert on {system.title}",
            goal=f"Find all possible causes for the fault {fault.title} in a {system.title}",
            backstory=dedent(
                f"""We have already identified that one of tha failures that can happen in a {system.title}
                is {fault.title} ({fault.description}). 
                Now we want to know the possible causes.
                """),
            llm=llm_model,
            max_iter=10,
            verbose=verbose
        )

    @classmethod
    def cause_merger_and_organizer(cls, causes, faults):

    @classmethod
    def indicator_researcher(cls, system: System, fault: Fault, cause: Cause, verbose=False):
        return Agent(
            role=f"Senior researcher that understand how we can detect the cause for failures in {system.title}",
            goal=dedent(
                f"""Find indications (called indicators) that we can look for when a {system.title} 
                has a failure of {fault.title} caused by {cause.title} ({cause.description})
                """),
            backstory=dedent(
                f"""We know that one of the failurs that can happen in {system.title} is {fault.title}
                caused by {cause.title}. 
                We now want to know what to look for to predict this.
                """),
            llm=llm_model,
            max_iter=10,
            verbose=verbose
        )

    @classmethod
    def sensor_researcher(cls, system: System, faults: List[Fault], causes: List[Cause], indicators: List[Indicator], verbose: bool = False):
        fault_bullet_list = "\n".join([f"* {fault.title}" for fault in faults])
        cause_bullet_list = "\n".join([f"* {cause.title}" for cause in causes])
        indicators_bullet_list = "\n".join([f"* {indicator.title}" for indicator in indicators])
        backstory = dedent(f"""We have identified a set of faults, causes, and indicators for {system.title}.
        These are the faults:
        {fault_bullet_list}
        These are the causes:
        {cause_bullet_list}
        These are the indicators:
        {indicators_bullet_list}
        """)
        return Agent(
            role=f"Senior researcher expert on sensors",
            goal=f"Find the sensors that help us understand the indicators",
            backstory=backstory,
            llm=llm_model,
            verbose=verbose
        )

    @classmethod
    def cause_deduplicator(cls, system: System, causes: List[Cause], verbose: bool = False):
        cause_bullet_list = '\n'.join([f"* [{c.id}] {c.title}: {c.description}" for c in causes])
        backstory = dedent(
            f"""
            We have identified a set of potential causes that can lead to failures in {system.title}.
            We have had different expert putting together their own list of causes. Their list is in the form:
            * [ID_OF_CAUSE] TITLE_OF_CAUSE: DESCRIPTION_OF_CAUSE
            
            E.g.:
            * [cause_id_a] Cause Name A: Description of cause A.
            * [cause_id_b] Cause Name B: Description of cause B.
            * ...
            """)
        goal = dedent(
            f"""
            We want to identify all duplicates and merge the duplicates in a way where we list the ids, the new name, 
            and produce a single description. 
            For example, if we have two causes that we believe to be duplicates, we want to produce:
            [CAUSE_ID_A, CAUSE_ID_B] Best Cause Name. Merged cause description for A and B.
            """)
        return Agent(
            role=f"Senior researcher that can identify when causes are the same for a {system.title}",
            backstory=backstory,
            goal=goal,
            llm=llm_model,
            verbose=verbose
        )