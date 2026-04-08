from pydantic import BaseModel
from typing import Dict, List, Any

class Action(BaseModel):
    command: str
    target: str

class Observation(BaseModel):
    services: Dict[str, str]
    incidents: List[Dict[str, Any]]
    metrics: Dict[str, int]
    steps: int

class Reward(BaseModel):
    score: float
