from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Profile
from app.schemas import ProfileCreate, ProfileUpdate, ProfileResponse, MessageResponse

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.get(
    "/",
    response_model=ProfileResponse,
    summary="Get Portfolio Owner Profile",
    description="Returns the complete profile of the portfolio owner including bio, social links, and contact information.",
)
def get_profile(db: Session = Depends(get_db)):
    profile = db.query(Profile).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found. Use POST /profile to create one.",
        )
    return profile


@router.post(
    "/",
    response_model=ProfileResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Portfolio Profile",
    description="Creates a new portfolio profile. Only one profile should exist.",
)
def create_profile(payload: ProfileCreate, db: Session = Depends(get_db)):
    existing = db.query(Profile).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A profile already exists. Use PATCH /profile to update it.",
        )
    profile = Profile(**payload.model_dump())
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


@router.patch(
    "/",
    response_model=ProfileResponse,
    summary="Update Portfolio Profile",
    description="Partially updates the portfolio profile. Only provided fields are updated.",
)
def update_profile(payload: ProfileUpdate, db: Session = Depends(get_db)):
    profile = db.query(Profile).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found. Use POST /profile to create one first.",
        )
    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(profile, field, value)
    db.commit()
    db.refresh(profile)
    return profile


@router.delete(
    "/",
    response_model=MessageResponse,
    summary="Delete Portfolio Profile",
    description="Permanently deletes the portfolio profile.",
)
def delete_profile(db: Session = Depends(get_db)):
    profile = db.query(Profile).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No profile found to delete.",
        )
    db.delete(profile)
    db.commit()
    return MessageResponse(message="Profile deleted successfully.")
