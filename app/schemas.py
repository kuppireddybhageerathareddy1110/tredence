from pydantic import BaseModel
from typing import Dict, Any, Optional


class GraphCreate(BaseModel):
    graph_id: Optional[str] = None
    type: Optional[str] = "code_review"
    params: Optional[Dict[str, Any]] = {}


class RunCreate(BaseModel):
    graph_id: str
    initial_state: Dict[str, Any]
