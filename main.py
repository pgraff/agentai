from typing import List, Set, ClassVar
from pydantic import BaseModel, Field
from crewai import Agent, Task, Crew, Process
from crewai_tools import BaseTool
# from langchain.llms import Ollama
from langchain_community.llms import Ollama

ollama_model = Ollama(model="llama2:13b")



# Pydantic models for Faults and Causes
class Fault(BaseModel):
    title: str = Field(title="A short name of the fault")
    description: str = Field(title="A deep description of the fault.")


class Faults(BaseModel):
    faults: List[Fault]


class Cause(BaseModel):
    title: str = Field(title="A short name for the cause")
    description: str = Field(title="A dseep description of the cause")

class Causes(BaseModel):
    causes: List[Cause] = Field(title="The list of causes")

class FaultWithCauses(BaseModel):
    title: str
    description: str
    causes: List[Cause]

fault_identification_agent = Agent(
    role="Expert on faults in steam engines",
    goal="Find all possible faults steam engine and return them as JSON",
    backstory="You are a world class expert on steam engines",
    verbose=True,
    allow_delegation=False,
    llm=ollama_model
)

cause_identification_agent = Agent(
    role="Expert on identifying causes for a given fault",
    goal="Find all possible causes for some fault",
    backstory="You are a world class expert identifying causes for a given fault on some equipment",
    verbose=True,
    allow_delegation=False,
    llm=ollama_model
)


# Function to identify faults (using Ollama)
def identify_faults() -> List[Fault]:
    prompt = "Identify possible faults for some equipment"
    response = query_ollama(prompt)
    # Process the response from Ollama to extract Fault objects
    # This is a placeholder, replace with your logic to parse Ollama's response
    return [Fault(title="Fault 1", description="Description of Fault 1")]


# Function to investigate a fault (using Ollama)
def investigate_fault(fault: Fault) -> List[Cause]:
    prompt = f"Investigate possible causes for the fault: {fault.title}"
    response = query_ollama(prompt)
    # Process the response from Ollama to extract Cause objects
    # This is a placeholder, replace with your logic to parse Ollama's response
    return [Cause(title="Cause 1", description="Description of Cause 1", faults={fault.title})]


# Task for fault identification
fault_identification_task = Task(
    description='Identify all possible faults of a steam engine.',
    agent=fault_identification_agent,
    output_pydantic=Faults,
    expected_output="""I want a complete list of faults in a simple list (no hierarchy)"""
)


# Setup Crew with the fault identification task
crew = Crew(
    agents=[fault_identification_agent],
    tasks=[fault_identification_task],
    process=Process.sequential
)

# Execute the crew to identify faults
faults = crew.kickoff()

print(faults)

list_of_fault_causes = []

for fault in faults.faults:
    print(f"Creating agent for: {fault.title}")
    investigation_task = Task(
        description=f'We have identified the fault {fault.title} for a steam engine. Investigate potential causes for {fault.title}',
        agent=cause_identification_agent,
        # func=lambda f=fault: investigate_fault(f),
        expected_output="An exhaustive list of causes",
        output_pydantic=Causes
    )
    # Add the investigation agent and task to the crew
    crew = Crew(
        agents=[cause_identification_agent],
        tasks=[investigation_task],
        process=Process.sequential
    )
    causes_list = crew.kickoff()
    list_of_fault_causes.append(
        FaultWithCauses.construct(
            title=fault.title,
            description=fault.description,
            causes=causes_list.causes
        )
    )


# Execute the crew to investigate causes
print(list_of_fault_causes)
