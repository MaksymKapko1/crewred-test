from datetime import date
from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship

class Place(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    external_id: int = Field(index=True)
    notes: Optional[str] = None
    is_visited: bool = Field(default=False)

    project_id: int = Field(foreign_key="travelproject.id")

    project: "TravelProject" = Relationship(back_populates="places")

class TravelProject(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    start_date: Optional[date] = None

    places: List[Place] = Relationship(
        back_populates="project",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )