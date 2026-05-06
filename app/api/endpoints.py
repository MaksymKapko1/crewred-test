from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from app.core.database import get_session
from app.models.models import TravelProject, Place
from app.models.schemas import ProjectCreate, PlaceUpdate, PlaceCreate
from app.services import validate_artwork

router = APIRouter()

@router.get("/projects", response_model=List[TravelProject])
async def get_projects(
        session: Session = Depends(get_session),
        offset: int = Query(default=0, ge=0, description="How many records to skip"),
        limit: int = Query(default=10, le=100, description="How many projects to restore (max 100)")
):
    projects = session.exec(
        select(TravelProject).offset(offset).limit(limit)
    ).all()
    return projects

@router.get("/projects/{project_id}", response_model=TravelProject)
async def get_project(project_id: int, session: Session = Depends(get_session)):
    project = session.get(TravelProject, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.get("/projects/{project_id}/places", response_model=List[Place])
async def get_project_places(project_id: int, session: Session = Depends(get_session)):
    project = session.get(TravelProject, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project.places

@router.post("/projects", response_model=TravelProject)
async def create_project(data: ProjectCreate, session: Session = Depends(get_session)):
    project = TravelProject(
        name=data.name,
        description=data.description,
        start_date=data.start_date,
    )
    session.add(project)
    session.commit()
    session.refresh(project)

    for external_id in data.places:
        await validate_artwork(external_id)
        place = Place(external_id=external_id, project_id=project.id)
        session.add(place)

    session.commit()
    session.refresh(project)
    return project

@router.post("/projects/{project_id}/places", response_model=Place)
async def add_place_to_project(
        project_id: int,
        data: PlaceCreate,
        session: Session = Depends(get_session)
):
    project = session.get(TravelProject, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if len(project.places) >= 10:
        raise HTTPException(status_code=400, detail="Maximum 10 places allowed per project")

    if any(p.external_id == data.external_id for p in project.places):
        raise HTTPException(status_code=400, detail="Place already exists in this project")

    await validate_artwork(data.external_id)

    place = Place(external_id=data.external_id, project_id=project.id)
    session.add(place)
    session.commit()
    session.refresh(place)
    return place

@router.patch("/projects/{project_id}/places/{place_id}", response_model=Place)
async def update_place(
        project_id: int,
        place_id: int,
        data: PlaceUpdate,
        session: Session = Depends(get_session),
):
    place = session.get(Place, place_id)

    if not place or place.project_id != project_id:
        raise HTTPException(status_code=404, detail="Place not found")

    if data.notes is not None:
        place.notes = data.notes
    if data.is_visited is not None:
        place.is_visited = data.is_visited

    session.add(place)
    session.commit()
    session.refresh(place)

    project = session.get(TravelProject, project_id)
    if project.places and all(p.is_visited for p in project.places):
        project.is_completed = True
        session.add(project)
        session.commit()

    return place

@router.delete("/projects/{project_id}")
async def delete_project(project_id: int, session: Session = Depends(get_session)):
    project = session.get(TravelProject, project_id)

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if any(place.is_visited for place in project.places):
        raise HTTPException(status_code=400, detail="Cannot delete project: it contains visited places")

    session.delete(project)
    session.commit()
    return {"detail": "Project deleted successfully"}