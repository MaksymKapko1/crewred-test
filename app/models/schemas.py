from datetime import date
from typing import Optional, List

from pydantic import BaseModel, Field

class PlaceCreate(BaseModel):
    external_id: int

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: Optional[date] = None
    places: List[int] = Field(default_factory=list, max_length=10)

class PlaceUpdate(BaseModel):
    notes: Optional[str] = None
    is_visited: Optional[bool] = None
