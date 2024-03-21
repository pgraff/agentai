from typing import List, Set, ClassVar
from pydantic import BaseModel, Field
from crewai import Agent, Task, Crew, Process

from fc_graph_agents import Agents
from fc_tasks import Tasks
from fc_model import System, FaultCauseResult, FaultWithCauses
import json

system = System.construct(
    title="steam engine",
    description="a machine using heat and the steam of from water to generate energy",
    goals="identify a fault cause graph for steam engines"
)

fault_agent = Agents.fault_researcher(system, verbose=True)
# Setup Crew with the fault identification task
crew = Crew(
    agents=[fault_agent],
    tasks=[Tasks.identify_faults(fault_agent, system)],
    process=Process.sequential
)

# Execute the crew to identify faults
faults = crew.kickoff()

print(faults)

result = FaultCauseResult.construct(system=system)

for fault in faults.items:
    print(f"Creating agent for: {fault.title}")
    cause_agent = Agents.cause_researcher(system, fault, verbose=True)
    cause_task = Tasks.identify_causes_for_a_fault(cause_agent, system, fault)
    # Add the investigation agent and task to the crew
    crew = Crew(
        agents=[cause_agent],
        tasks=[cause_task],
        process=Process.sequential
    )
    causes_list = crew.kickoff()
    result.faults_and_causes.append(
        FaultWithCauses.construct(
            title=fault.title,
            description=fault.description,
            causes=causes_list.items
        )
    )


# Execute the crew to investigate causes
print(result)
print(result.model_dump_json(indent=2))
