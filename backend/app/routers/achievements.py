from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Achievement
from app.schemas import AchievementCreate, AchievementUpdate, AchievementResponse, MessageResponse

router = APIRouter(prefix="/achievements", tags=["Achievements"])


@router.get(
    "/",
    response_model=List[AchievementResponse],
    summary="Get All Achievements",
    description="Returns all achievement records sorted by order.",
)
def get_all_achievements(db: Session = Depends(get_db)):
    return db.query(Achievement).order_by(Achievement.order).all()


@router.get(
    "/{achievement_id}",
    response_model=AchievementResponse,
    summary="Get Single Achievement",
    description="Returns a single achievement entry by its ID.",
)
def get_achievement(achievement_id: int, db: Session = Depends(get_db)):
    record = db.query(Achievement).filter(Achievement.id == achievement_id).first()
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Achievement with ID {achievement_id} not found.",
        )
    return record


@router.post(
    "/",
    response_model=AchievementResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add Achievement",
    description="Creates a new achievement entry.",
)
def create_achievement(payload: AchievementCreate, db: Session = Depends(get_db)):
    record = Achievement(**payload.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.patch(
    "/{achievement_id}",
    response_model=AchievementResponse,
    summary="Update Achievement",
    description="Partially updates an achievement by its ID.",
)
def update_achievement(achievement_id: int, payload: AchievementUpdate, db: Session = Depends(get_db)):
    record = db.query(Achievement).filter(Achievement.id == achievement_id).first()
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Achievement with ID {achievement_id} not found.",
        )
    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(record, field, value)
    db.commit()
    db.refresh(record)
    return record


@router.delete(
    "/{achievement_id}",
    response_model=MessageResponse,
    summary="Delete Achievement",
    description="Permanently deletes an achievement entry by its ID.",
)
def delete_achievement(achievement_id: int, db: Session = Depends(get_db)):
    record = db.query(Achievement).filter(Achievement.id == achievement_id).first()
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Achievement with ID {achievement_id} not found.",
        )
    db.delete(record)
    db.commit()
    return MessageResponse(message=f"Achievement {achievement_id} deleted successfully.")
