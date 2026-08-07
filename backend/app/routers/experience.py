from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models import Experience
from app.schemas import ExperienceCreate, ExperienceUpdate, ExperienceResponse, MessageResponse

router = APIRouter(prefix="/experience", tags=["Experience"])


@router.get(
    "/",
    response_model=List[ExperienceResponse],
    summary="Get All Experience Entries",
    description="Returns all experience entries sorted by order. Filter by employment_type or is_current.",
)
def get_all_experience(
    employment_type: Optional[str] = Query(None, description="Filter by type: Internship, Part-time, Full-time, Training"),
    is_current: Optional[bool] = Query(None, description="Filter by current employment status"),
    db: Session = Depends(get_db),
):
    query = db.query(Experience)
    if employment_type:
        query = query.filter(Experience.employment_type == employment_type)
    if is_current is not None:
        query = query.filter(Experience.is_current == is_current)
    return query.order_by(Experience.order).all()


@router.get(
    "/{experience_id}",
    response_model=ExperienceResponse,
    summary="Get Single Experience Entry",
    description="Returns a single experience entry by its ID.",
)
def get_experience(experience_id: int, db: Session = Depends(get_db)):
    record = db.query(Experience).filter(Experience.id == experience_id).first()
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Experience entry with ID {experience_id} not found.",
        )
    return record


@router.post(
    "/",
    response_model=ExperienceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add Experience Entry",
    description="Creates a new work experience entry with responsibilities and technologies.",
)
def create_experience(payload: ExperienceCreate, db: Session = Depends(get_db)):
    record = Experience(**payload.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.patch(
    "/{experience_id}",
    response_model=ExperienceResponse,
    summary="Update Experience Entry",
    description="Partially updates a work experience entry by its ID.",
)
def update_experience(experience_id: int, payload: ExperienceUpdate, db: Session = Depends(get_db)):
    record = db.query(Experience).filter(Experience.id == experience_id).first()
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Experience entry with ID {experience_id} not found.",
        )
    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(record, field, value)
    db.commit()
    db.refresh(record)
    return record


@router.delete(
    "/{experience_id}",
    response_model=MessageResponse,
    summary="Delete Experience Entry",
    description="Permanently deletes a work experience entry by its ID.",
)
def delete_experience(experience_id: int, db: Session = Depends(get_db)):
    record = db.query(Experience).filter(Experience.id == experience_id).first()
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Experience entry with ID {experience_id} not found.",
        )
    db.delete(record)
    db.commit()
    return MessageResponse(message=f"Experience entry {experience_id} deleted successfully.")
