from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class EventOutcome(BaseModel):
    probability: float
    result_text: str
    stat_changes: Dict[str, int]

class EventOption(BaseModel):
    option_id: str
    text: str
    required_cyber_sense: int = 0
    outcomes: List[EventOutcome]

class EventSchema(BaseModel):
    event_id: str
    event_type: str = "routine"
    tags: List[str] = []
    is_unique: bool = False
    weight: int = 10
    prerequisites: Dict[str, Any] = {}
    
    title: str
    description: str
    technical_context: str
    options: List[EventOption]
    
    timeout_seconds: Optional[int] = None
    timeout_option_id: Optional[str] = None
