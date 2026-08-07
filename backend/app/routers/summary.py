from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Profile, Education, Experience, Skill, Certification, Project, Achievement

router = APIRouter(prefix="/summary", tags=["Summary"])


@router.get(
    "/",
    summary="Get Full Portfolio Summary",
    description=(
        "Returns a single consolidated JSON response containing all portfolio sections. "
        "Ideal for the frontend to fetch everything in one request on initial load."
    ),
)
def get_portfolio_summary(db: Session = Depends(get_db)):
    profile = db.query(Profile).first()
    education = db.query(Education).order_by(Education.order).all()
    experience = db.query(Experience).order_by(Experience.order).all()
    skills = db.query(Skill).order_by(Skill.category, Skill.order).all()
    certifications = db.query(Certification).order_by(Certification.order).all()
    projects = db.query(Project).order_by(Project.order).all()
    achievements = db.query(Achievement).order_by(Achievement.order).all()

    # Build grouped skills
    grouped_skills: dict = {}
    for skill in skills:
        cat = skill.category
        if cat not in grouped_skills:
            grouped_skills[cat] = []
        grouped_skills[cat].append({
            "id": skill.id,
            "name": skill.name,
            "proficiency": skill.proficiency,
            "icon": skill.icon,
        })

    def serialize_model(obj):
        """Convert a SQLAlchemy model to a dict, excluding internal state."""
        return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}

    return {
        "profile": serialize_model(profile) if profile else None,
        "education": [serialize_model(e) for e in education],
        "experience": [serialize_model(e) for e in experience],
        "skills": grouped_skills,
        "certifications": [serialize_model(c) for c in certifications],
        "projects": [serialize_model(p) for p in projects],
        "achievements": [serialize_model(a) for a in achievements],
        "stats": {
            "total_projects": len(projects),
            "featured_projects": sum(1 for p in projects if p.is_featured),
            "total_skills": len(skills),
            "skill_categories": len(grouped_skills),
            "total_certifications": len(certifications),
            "total_achievements": len(achievements),
            "years_of_experience": len(experience),
        },
    }
