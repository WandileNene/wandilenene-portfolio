from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict
from app.database import get_db
from app.models import Skill
from app.schemas import SkillCreate, SkillUpdate, SkillResponse, MessageResponse

router = APIRouter(prefix="/skills", tags=["Skills"])


@router.get(
    "/",
    response_model=List[SkillResponse],
    summary="Get All Skills",
    description="Returns all skills. Optionally filter by category.",
)
def get_all_skills(
    category: Optional[str] = Query(None, description="Filter by category name"),
    db: Session = Depends(get_db),
):
    query = db.query(Skill)
    if category:
        query = query.filter(Skill.category == category)
    return query.order_by(Skill.category, Skill.order).all()


@router.get(
    "/grouped",
    summary="Get Skills Grouped by Category",
    description="Returns all skills organized as a dictionary grouped by category. Ideal for rendering skill section UI.",
)
def get_skills_grouped(db: Session = Depends(get_db)):
    skills = db.query(Skill).order_by(Skill.category, Skill.order).all()
    grouped: Dict[str, List[dict]] = {}
    for skill in skills:
        cat = skill.category
        if cat not in grouped:
            grouped[cat] = []
        grouped[cat].append({
            "id": skill.id,
            "name": skill.name,
            "proficiency": skill.proficiency,
            "icon": skill.icon,
            "order": skill.order,
        })
    return {"categories": grouped}


@router.get(
    "/categories",
    summary="Get All Skill Categories",
    description="Returns a list of all unique skill category names.",
)
def get_skill_categories(db: Session = Depends(get_db)):
    rows = db.query(Skill.category).distinct().order_by(Skill.category).all()
    return {"categories": [row[0] for row in rows]}


@router.get(
    "/{skill_id}",
    response_model=SkillResponse,
    summary="Get Single Skill",
    description="Returns a single skill entry by its ID.",
)
def get_skill(skill_id: int, db: Session = Depends(get_db)):
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Skill with ID {skill_id} not found.",
        )
    return skill


@router.post(
    "/",
    response_model=SkillResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add a Skill",
    description="Creates a new skill entry with category and proficiency level (0–100).",
)
def create_skill(payload: SkillCreate, db: Session = Depends(get_db)):
    skill = Skill(**payload.model_dump())
    db.add(skill)
    db.commit()
    db.refresh(skill)
    return skill


@router.patch(
    "/{skill_id}",
    response_model=SkillResponse,
    summary="Update a Skill",
    description="Partially updates a skill entry by its ID.",
)
def update_skill(skill_id: int, payload: SkillUpdate, db: Session = Depends(get_db)):
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Skill with ID {skill_id} not found.",
        )
    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(skill, field, value)
    db.commit()
    db.refresh(skill)
    return skill


@router.delete(
    "/{skill_id}",
    response_model=MessageResponse,
    summary="Delete a Skill",
    description="Permanently deletes a skill entry by its ID.",
)
def delete_skill(skill_id: int, db: Session = Depends(get_db)):
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Skill with ID {skill_id} not found.",
        )
    db.delete(skill)
    db.commit()
    return MessageResponse(message=f"Skill {skill_id} deleted successfully.")
