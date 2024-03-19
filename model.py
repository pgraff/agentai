from pydantic import BaseModel
from typing import List, Set

class Fault(BaseModel):
    title: str
    description: str

class Cause(BaseModel):
    title: str
    description: str
    faults: Set[str]  # Using set to avoid duplicate fault titles

