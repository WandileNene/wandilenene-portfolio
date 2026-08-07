from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import shutil
from datetime import datetime
from pathlib import Path

from app.database import get_db
from app.models import Resume
from app.schemas import ResumeResponse, MessageResponse

router = APIRouter(prefix="/resume", tags=["Resume"])

# Upload directory for resumes
UPLOAD_DIR = Path("uploads/resumes")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".doc"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


def validate_resume_file(file: UploadFile) -> None:
    """Validate that the uploaded file is a valid resume format."""
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}",
        )


@router.post(
    "/upload",
    response_model=ResumeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload Resume File",
    description=(
        "Upload a resume file (PDF, DOCX). The file is saved and metadata stored in the database. "
        "Only one resume can be active at a time."
    ),
)
async def upload_resume(
    file: UploadFile = File(..., description="Resume file (PDF or DOCX)"),
    version: Optional[str] = Form(None, description="Version label (e.g., v2.0, 2024-08)"),
    description: Optional[str] = Form(None, description="Description of this resume version"),
    db: Session = Depends(get_db),
):
    validate_resume_file(file)

    # Generate unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    ext = Path(file.filename).suffix
    filename = f"resume_{timestamp}{ext}"
    file_path = UPLOAD_DIR / filename

    # Save file
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save file: {str(e)}",
        )

    # Get file size
    file_size = os.path.getsize(file_path)

    if file_size > MAX_FILE_SIZE:
        os.remove(file_path)
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Maximum size is {MAX_FILE_SIZE / (1024*1024)}MB",
        )

    # Deactivate all other resumes
    db.query(Resume).update({"is_active": False})

    # Create resume record
    resume = Resume(
        filename=filename,
        original_filename=file.filename,
        file_path=str(file_path),
        file_size=file_size,
        content_type=file.content_type or "application/octet-stream",
        version=version,
        description=description,
        is_active=True,
    )
    db.add(resume)
    db.commit()
    db.refresh(resume)

    return resume


@router.get(
    "/",
    response_model=ResumeResponse,
    summary="Get Active Resume Metadata",
    description="Returns metadata for the currently active resume (filename, size, version, etc.).",
)
def get_active_resume(db: Session = Depends(get_db)):
    resume = db.query(Resume).filter(Resume.is_active == True).first()
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active resume found. Upload one using POST /resume/upload",
        )
    return resume


@router.get(
    "/all",
    response_model=List[ResumeResponse],
    summary="Get All Resume Versions",
    description="Returns metadata for all resume versions (active and inactive).",
)
def get_all_resumes(db: Session = Depends(get_db)):
    return db.query(Resume).order_by(Resume.created_at.desc()).all()


@router.get(
    "/download",
    summary="Download Active Resume File",
    description="Downloads the currently active resume file as an attachment.",
    responses={
        200: {
            "content": {"application/pdf": {}, "application/vnd.openxmlformats-officedocument.wordprocessingml.document": {}},
            "description": "Resume file download",
        }
    },
)
def download_active_resume(db: Session = Depends(get_db)):
    resume = db.query(Resume).filter(Resume.is_active == True).first()
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active resume available for download.",
        )

    file_path = Path(resume.file_path)
    if not file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume file not found on server.",
        )

    return FileResponse(
        path=str(file_path),
        media_type=resume.content_type,
        filename=resume.original_filename,
    )


@router.get(
    "/download/{resume_id}",
    summary="Download Specific Resume by ID",
    description="Downloads a specific resume version by its ID.",
)
def download_resume_by_id(resume_id: int, db: Session = Depends(get_db)):
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resume with ID {resume_id} not found.",
        )

    file_path = Path(resume.file_path)
    if not file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume file not found on server.",
        )

    return FileResponse(
        path=str(file_path),
        media_type=resume.content_type,
        filename=resume.original_filename,
    )


@router.patch(
    "/{resume_id}/activate",
    response_model=ResumeResponse,
    summary="Set a Resume as Active",
    description="Makes a specific resume version the active one. Deactivates all others.",
)
def activate_resume(resume_id: int, db: Session = Depends(get_db)):
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resume with ID {resume_id} not found.",
        )

    # Deactivate all
    db.query(Resume).update({"is_active": False})
    # Activate this one
    resume.is_active = True
    db.commit()
    db.refresh(resume)
    return resume


@router.delete(
    "/{resume_id}",
    response_model=MessageResponse,
    summary="Delete Resume",
    description="Deletes a resume entry and its file from the server.",
)
def delete_resume(resume_id: int, db: Session = Depends(get_db)):
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resume with ID {resume_id} not found.",
        )

    # Delete file from disk
    file_path = Path(resume.file_path)
    if file_path.exists():
        try:
            os.remove(file_path)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete file: {str(e)}",
            )

    # Delete DB record
    db.delete(resume)
    db.commit()

    return MessageResponse(message=f"Resume {resume_id} deleted successfully.")
