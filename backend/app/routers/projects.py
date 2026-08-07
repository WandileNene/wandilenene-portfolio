from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models import Project
from app.schemas import ProjectCreate, ProjectUpdate, ProjectResponse, MessageResponse

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.get(
    "/",
    response_model=List[ProjectResponse],
    summary="Get All Projects",
    description="Returns all projects. Filter by featured status or project status.",
)
def get_all_projects(
    featured: Optional[bool] = Query(None, description="Filter to only featured projects"),
    project_status: Optional[str] = Query(None, alias="status", description="Filter by status: completed, in-progress, archived"),
    db: Session = Depends(get_db),
):
    query = db.query(Project)
    if featured is not None:
        query = query.filter(Project.is_featured == featured)
    if project_status:
        query = query.filter(Project.status == project_status)
    return query.order_by(Project.order).all()


@router.get(
    "/featured",
    response_model=List[ProjectResponse],
    summary="Get Featured Projects",
    description="Returns only projects marked as featured. Use this for the homepage showcase.",
)
def get_featured_projects(db: Session = Depends(get_db)):
    return db.query(Project).filter(Project.is_featured == True).order_by(Project.order).all()


@router.get(
    "/slug/{slug}",
    response_model=ProjectResponse,
    summary="Get Project by Slug",
    description="Returns a single project by its URL-friendly slug.",
)
def get_project_by_slug(slug: str, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.slug == slug).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with slug '{slug}' not found.",
        )
    return project


@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Get Project by ID",
    description="Returns a single project by its numeric ID.",
)
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID {project_id} not found.",
        )
    return project


@router.post(
    "/",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add Project",
    description="Creates a new project entry with technologies, features, and links.",
)
def create_project(payload: ProjectCreate, db: Session = Depends(get_db)):
    existing = db.query(Project).filter(Project.slug == payload.slug).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"A project with slug '{payload.slug}' already exists.",
        )
    project = Project(**payload.model_dump())
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@router.patch(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Update Project",
    description="Partially updates a project entry by its ID.",
)
def update_project(project_id: int, payload: ProjectUpdate, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID {project_id} not found.",
        )
    # Check slug uniqueness if being updated
    if payload.slug and payload.slug != project.slug:
        slug_conflict = db.query(Project).filter(Project.slug == payload.slug).first()
        if slug_conflict:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"A project with slug '{payload.slug}' already exists.",
            )
    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(project, field, value)
    db.commit()
    db.refresh(project)
    return project


@router.delete(
    "/{project_id}",
    response_model=MessageResponse,
    summary="Delete Project",
    description="Permanently deletes a project entry by its ID.",
)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID {project_id} not found.",
        )
    db.delete(project)
    db.commit()
    return MessageResponse(message=f"Project {project_id} deleted successfully.")
