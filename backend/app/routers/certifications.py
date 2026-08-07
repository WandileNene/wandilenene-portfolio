from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Certification
from app.schemas import CertificationCreate, CertificationUpdate, CertificationResponse, MessageResponse

router = APIRouter(prefix="/certifications", tags=["Certifications"])


@router.get(
    "/",
    response_model=List[CertificationResponse],
    summary="Get All Certifications",
    description="Returns all certifications sorted by order.",
)
def get_all_certifications(db: Session = Depends(get_db)):
    return db.query(Certification).order_by(Certification.order).all()


@router.get(
    "/{cert_id}",
    response_model=CertificationResponse,
    summary="Get Single Certification",
    description="Returns a single certification by its ID.",
)
def get_certification(cert_id: int, db: Session = Depends(get_db)):
    cert = db.query(Certification).filter(Certification.id == cert_id).first()
    if not cert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Certification with ID {cert_id} not found.",
        )
    return cert


@router.post(
    "/",
    response_model=CertificationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add Certification",
    description="Creates a new certification entry with issuing org, dates, and optional credential URL.",
)
def create_certification(payload: CertificationCreate, db: Session = Depends(get_db)):
    cert = Certification(**payload.model_dump())
    db.add(cert)
    db.commit()
    db.refresh(cert)
    return cert


@router.patch(
    "/{cert_id}",
    response_model=CertificationResponse,
    summary="Update Certification",
    description="Partially updates a certification entry by its ID.",
)
def update_certification(cert_id: int, payload: CertificationUpdate, db: Session = Depends(get_db)):
    cert = db.query(Certification).filter(Certification.id == cert_id).first()
    if not cert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Certification with ID {cert_id} not found.",
        )
    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(cert, field, value)
    db.commit()
    db.refresh(cert)
    return cert


@router.delete(
    "/{cert_id}",
    response_model=MessageResponse,
    summary="Delete Certification",
    description="Permanently deletes a certification entry by its ID.",
)
def delete_certification(cert_id: int, db: Session = Depends(get_db)):
    cert = db.query(Certification).filter(Certification.id == cert_id).first()
    if not cert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Certification with ID {cert_id} not found.",
        )
    db.delete(cert)
    db.commit()
    return MessageResponse(message=f"Certification {cert_id} deleted successfully.")
