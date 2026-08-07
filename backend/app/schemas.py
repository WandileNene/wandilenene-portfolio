from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


# Profile Schemas
class ProfileBase(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=255)
    title: str = Field(..., min_length=1, max_length=255)
    tagline: Optional[str] = None
    bio: Optional[str] = None
    profile_image: Optional[str] = None
    email: EmailStr
    phone: Optional[str] = None
    location: Optional[str] = None
    github_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    twitter_url: Optional[str] = None


class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=1, max_length=255)
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    tagline: Optional[str] = None
    bio: Optional[str] = None
    profile_image: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    github_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    twitter_url: Optional[str] = None


class ProfileResponse(ProfileBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Education Schemas
class EducationBase(BaseModel):
    degree: str = Field(..., min_length=1, max_length=255)
    field_of_study: str = Field(..., min_length=1, max_length=255)
    institution: str = Field(..., min_length=1, max_length=255)
    location: Optional[str] = None
    start_date: str
    end_date: Optional[str] = None
    grade: Optional[str] = None
    description: Optional[str] = None
    is_current: bool = False
    order: int = 0


class EducationCreate(EducationBase):
    pass


class EducationUpdate(BaseModel):
    degree: Optional[str] = Field(None, min_length=1, max_length=255)
    field_of_study: Optional[str] = Field(None, min_length=1, max_length=255)
    institution: Optional[str] = Field(None, min_length=1, max_length=255)
    location: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    grade: Optional[str] = None
    description: Optional[str] = None
    is_current: Optional[bool] = None
    order: Optional[int] = None


class EducationResponse(EducationBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Experience Schemas
class ExperienceBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    company: str = Field(..., min_length=1, max_length=255)
    location: Optional[str] = None
    employment_type: Optional[str] = None
    start_date: str
    end_date: Optional[str] = None
    is_current: bool = False
    description: Optional[str] = None
    responsibilities: Optional[List[str]] = None
    technologies: Optional[List[str]] = None
    order: int = 0


class ExperienceCreate(ExperienceBase):
    pass


class ExperienceUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    company: Optional[str] = Field(None, min_length=1, max_length=255)
    location: Optional[str] = None
    employment_type: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    is_current: Optional[bool] = None
    description: Optional[str] = None
    responsibilities: Optional[List[str]] = None
    technologies: Optional[List[str]] = None
    order: Optional[int] = None


class ExperienceResponse(ExperienceBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Skill Schemas
class SkillBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    category: str = Field(..., min_length=1, max_length=100)
    proficiency: int = Field(default=0, ge=0, le=100)
    icon: Optional[str] = None
    order: int = 0


class SkillCreate(SkillBase):
    pass


class SkillUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    proficiency: Optional[int] = Field(None, ge=0, le=100)
    icon: Optional[str] = None
    order: Optional[int] = None


class SkillResponse(SkillBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Certification Schemas
class CertificationBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    issuing_organization: str = Field(..., min_length=1, max_length=255)
    issue_date: str
    expiry_date: Optional[str] = None
    credential_id: Optional[str] = None
    credential_url: Optional[str] = None
    description: Optional[str] = None
    order: int = 0


class CertificationCreate(CertificationBase):
    pass


class CertificationUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    issuing_organization: Optional[str] = Field(None, min_length=1, max_length=255)
    issue_date: Optional[str] = None
    expiry_date: Optional[str] = None
    credential_id: Optional[str] = None
    credential_url: Optional[str] = None
    description: Optional[str] = None
    order: Optional[int] = None


class CertificationResponse(CertificationBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Project Schemas
class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    slug: str = Field(..., min_length=1, max_length=255)
    short_description: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = None
    technologies: Optional[List[str]] = None
    features: Optional[List[str]] = None
    github_url: Optional[str] = None
    demo_url: Optional[str] = None
    image_url: Optional[str] = None
    status: str = "completed"
    is_featured: bool = False
    order: int = 0


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    slug: Optional[str] = Field(None, min_length=1, max_length=255)
    short_description: Optional[str] = Field(None, min_length=1, max_length=500)
    description: Optional[str] = None
    technologies: Optional[List[str]] = None
    features: Optional[List[str]] = None
    github_url: Optional[str] = None
    demo_url: Optional[str] = None
    image_url: Optional[str] = None
    status: Optional[str] = None
    is_featured: Optional[bool] = None
    order: Optional[int] = None


class ProjectResponse(ProjectBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Achievement Schemas
class AchievementBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    issuer: str = Field(..., min_length=1, max_length=255)
    date: str
    description: Optional[str] = None
    icon: Optional[str] = None
    order: int = 0


class AchievementCreate(AchievementBase):
    pass


class AchievementUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    issuer: Optional[str] = Field(None, min_length=1, max_length=255)
    date: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    order: Optional[int] = None


class AchievementResponse(AchievementBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Contact Message Schemas
class ContactMessageBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    subject: Optional[str] = None
    message: str = Field(..., min_length=1)


class ContactMessageCreate(ContactMessageBase):
    pass


class ContactMessageResponse(ContactMessageBase):
    id: int
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True


# Resume Schemas
class ResumeBase(BaseModel):
    version: Optional[str] = None
    description: Optional[str] = None
    is_active: bool = True


class ResumeResponse(BaseModel):
    id: int
    filename: str
    original_filename: str
    file_size: int
    content_type: str
    version: Optional[str] = None
    description: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Generic Response Schemas
class MessageResponse(BaseModel):
    message: str
    detail: Optional[str] = None


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
