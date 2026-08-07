from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Education
from app.schemas import EducationCreate, EducationUpdate, EducationResponse, MessageResponse

router = APIRouter(prefix="/education", tags=["Education"])


@router.get(
    "/",
    response_model=List[EducationResponse],
    summary="Get All Education Records",
    description="Returns all education records sorted by the order field.",
)
def get_all_education(db: Session = Depends(get_db)):
    records = db.query(Education).order_by(Education.order).all()
    return records


@router.get(
    "/{education_id}",
    response_model=EducationResponse,
    summary="Get Single Education Record",
    description="Returns a single education record by its ID.",
)
def get_education(education_id: int, db: Session = Depends(get_db)):
    record = db.query(Education).filter(Education.id == education_id).first()
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Education record with ID {education_id} not found.",
        )
    return record


@router.post(
    "/",
    response_model=EducationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add Education Record",
    description="Creates a new education entry (degree, institution, dates, etc.).",
)
def create_education(payload: EducationCreate, db: Session = Depends(get_db)):
    record = Education(**payload.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.patch(
    "/{education_id}",
    response_model=EducationResponse,
    summary="Update Education Record",
    description="Partially updates an education record by its ID.",
)
def update_education(education_id: int, payload: EducationUpdate, db: Session = Depends(get_db)):
    record = db.query(Education).filter(Education.id == education_id).first()
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Education record with ID {education_id} not found.",
        )
    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(record, field, value)
    db.commit()
    db.refresh(record)
    return record


@router.delete(
    "/{education_id}",
    response_model=MessageResponse,
    summary="Delete Education Record",
    description="Permanently deletes an education record by its ID.",
)
def delete_education(education_id: int, db: Session = Depends(get_db)):
    record = db.query(Education).filter(Education.id == education_id).first()
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Education record with ID {education_id} not found.",
        )
    db.delete(record)
    db.commit()
    return MessageResponse(message=f"Education record {education_id} deleted successfully.")
