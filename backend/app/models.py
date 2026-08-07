from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Profile(Base):
    """User profile and about information"""
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    title = Column(String(255), nullable=False)
    tagline = Column(Text, nullable=True)
    bio = Column(Text, nullable=True)
    profile_image = Column(String(500), nullable=True)
    email = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=True)
    location = Column(String(255), nullable=True)
    github_url = Column(String(500), nullable=True)
    linkedin_url = Column(String(500), nullable=True)
    twitter_url = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Education(Base):
    """Education records"""
    __tablename__ = "education"

    id = Column(Integer, primary_key=True, index=True)
    degree = Column(String(255), nullable=False)
    field_of_study = Column(String(255), nullable=False)
    institution = Column(String(255), nullable=False)
    location = Column(String(255), nullable=True)
    start_date = Column(String(50), nullable=False)
    end_date = Column(String(50), nullable=True)
    grade = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    is_current = Column(Boolean, default=False)
    order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Experience(Base):
    """Work experience and internships"""
    __tablename__ = "experiences"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    company = Column(String(255), nullable=False)
    location = Column(String(255), nullable=True)
    employment_type = Column(String(100), nullable=True)  # Full-time, Intern, Contract
    start_date = Column(String(50), nullable=False)
    end_date = Column(String(50), nullable=True)
    is_current = Column(Boolean, default=False)
    description = Column(Text, nullable=True)
    responsibilities = Column(JSON, nullable=True)  # List of responsibilities
    technologies = Column(JSON, nullable=True)  # List of technologies used
    order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Skill(Base):
    """Technical skills"""
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)  # Languages, Frameworks, Tools, etc.
    proficiency = Column(Integer, default=0)  # 0-100
    icon = Column(String(255), nullable=True)
    order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Certification(Base):
    """Professional certifications"""
    __tablename__ = "certifications"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    issuing_organization = Column(String(255), nullable=False)
    issue_date = Column(String(50), nullable=False)
    expiry_date = Column(String(50), nullable=True)
    credential_id = Column(String(255), nullable=True)
    credential_url = Column(String(500), nullable=True)
    description = Column(Text, nullable=True)
    order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Project(Base):
    """Portfolio projects"""
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    short_description = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    technologies = Column(JSON, nullable=True)  # List of technologies
    features = Column(JSON, nullable=True)  # List of key features
    github_url = Column(String(500), nullable=True)
    demo_url = Column(String(500), nullable=True)
    image_url = Column(String(500), nullable=True)
    status = Column(String(50), default="completed")  # completed, in-progress, archived
    is_featured = Column(Boolean, default=False)
    order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Achievement(Base):
    """Awards and achievements"""
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    issuer = Column(String(255), nullable=False)
    date = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    icon = Column(String(255), nullable=True)
    order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ContactMessage(Base):
    """Contact form messages"""
    __tablename__ = "contact_messages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    subject = Column(String(500), nullable=True)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Resume(Base):
    """Resume file metadata and storage"""
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer, nullable=False)  # in bytes
    content_type = Column(String(100), nullable=False)
    version = Column(String(50), nullable=True)  # e.g., "v2.0", "2024-08"
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
