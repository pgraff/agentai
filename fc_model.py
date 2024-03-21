from pydantic import BaseModel, Field
from typing import List
from tools import generate_id


class System(BaseModel):
    title: str = Field(title="A short name")
    description: str = Field(title="A longer description")
    goals: str = Field(title="The overall goal we have for the system")


class Fault(BaseModel):
    title: str = Field(title="A short name for the fault")
    description: str = Field(title="A deeper description for the fault")


class Faults(BaseModel):
    items: List[Fault] = Field(title="A list of the faults")


class Cause(BaseModel):
    title: str = Field(title="A short name for the cause")
    description: str = Field(title="A deeper description of the cause")


class Causes(BaseModel):
    items: List[Cause] = Field(title="A list of causes")


class Indicator(BaseModel):
    id: str = Field(title="A unique identifier")
    title: str = Field(title="A short name for the indicator")
    description: str = Field(title="A deeper description of the indicator")


class Indicators(BaseModel):
    items: List[Cause] = Field(title="A list of indicators")


class Sensor(BaseModel):
    id: str = Field(title="A unique identifier")
    title: str = Field(title="A short name for the sensor")
    description: str = Field(title="A deeper description of the sensors")
    role: str = Field(title="Exactly what this sensor is being used for")


class Sensors(BaseModel):
    items: List[Cause] = Field(title="A list of sensors")


class FaultWithCauses(BaseModel):
    title: str
    description: str
    causes: List[Cause]


class FaultCauseResult(BaseModel):
    system: System
    faults_and_causes: List[FaultWithCauses] = []

class MergedCause(BaseModel):
    ids: List[str] = Field(description="A list of the input cause identifiers")
    title: str = Field(description="A short name for the cause")
    description: str = Field(description="A deeper definition of the cause")

class MergedCausesResult(BaseModel):
    causes: List[MergedCause] = Field(description="A list of the merged causes")