"""
Pytest configuration and shared fixtures for testing.
Creates isolated test database and client for each test.
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from httpx import AsyncClient, ASGITransport
from typing import Generator, AsyncGenerator
from faker import Faker

from app.database import Base, get_db
from app.main import app
from app.models import (
    Profile, Education, Experience, Skill, 
    Certification, Project, Achievement, ContactMessage, Resume
)

# Create in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# Create engine with special config for in-memory SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # Keep the same connection for all threads
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db() -> Generator:
    """
    Create a fresh database for each test function.
    Yields a database session and cleans up after the test.
    """
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create session
    session = TestingSessionLocal()
    
    try:
        yield session
    finally:
        session.close()
        # Drop all tables after test
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
async def client(db) -> AsyncGenerator:
    """
    Create an async test client with overridden database dependency.
    """
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    
    app.dependency_overrides.clear()


@pytest.fixture
def fake() -> Faker:
    """Faker instance for generating test data."""
    return Faker()


# ============================================================================
# FACTORY FIXTURES - Create sample data for testing
# ============================================================================

@pytest.fixture
def sample_profile_data(fake) -> dict:
    """Generate sample profile data."""
    return {
        "full_name": fake.name(),
        "title": fake.job(),
        "tagline": fake.catch_phrase(),
        "bio": fake.text(max_nb_chars=500),
        "email": fake.email(),
        "phone": fake.phone_number(),
        "location": fake.city(),
        "github_url": f"https://github.com/{fake.user_name()}",
        "linkedin_url": f"https://linkedin.com/in/{fake.user_name()}",
    }


@pytest.fixture
def sample_education_data(fake) -> dict:
    """Generate sample education data."""
    return {
        "degree": "Bachelor of Science",
        "field_of_study": "Computer Science",
        "institution": fake.company(),
        "location": fake.city(),
        "start_date": "2018-09",
        "end_date": "2022-05",
        "grade": "3.8 GPA",
        "description": fake.text(max_nb_chars=200),
        "is_current": False,
        "order": 0,
    }


@pytest.fixture
def sample_experience_data(fake) -> dict:
    """Generate sample experience data."""
    return {
        "title": "Software Engineer",
        "company": fake.company(),
        "location": fake.city(),
        "employment_type": "Full-time",
        "start_date": "2022-06",
        "end_date": None,
        "is_current": True,
        "description": fake.text(max_nb_chars=300),
        "responsibilities": [
            "Developed web applications",
            "Collaborated with team members",
            "Maintained code quality",
        ],
        "technologies": ["Python", "FastAPI", "React", "PostgreSQL"],
        "order": 0,
    }


@pytest.fixture
def sample_skill_data(fake) -> dict:
    """Generate sample skill data."""
    return {
        "name": "Python",
        "category": "Languages",
        "proficiency": 85,
        "icon": "python-icon",
        "order": 0,
    }


@pytest.fixture
def sample_certification_data(fake) -> dict:
    """Generate sample certification data."""
    return {
        "name": "AWS Solutions Architect",
        "issuing_organization": "Amazon Web Services",
        "issue_date": "2024-01",
        "expiry_date": "2027-01",
        "credential_id": fake.uuid4(),
        "credential_url": f"https://aws.amazon.com/verify/{fake.uuid4()}",
        "description": fake.text(max_nb_chars=200),
        "order": 0,
    }


@pytest.fixture
def sample_project_data(fake) -> dict:
    """Generate sample project data."""
    slug = fake.slug()
    return {
        "name": fake.catch_phrase(),
        "slug": slug,
        "short_description": fake.text(max_nb_chars=100),
        "description": fake.text(max_nb_chars=500),
        "technologies": ["Python", "FastAPI", "React"],
        "features": ["Feature 1", "Feature 2", "Feature 3"],
        "github_url": f"https://github.com/user/{slug}",
        "demo_url": f"https://{slug}.demo.com",
        "image_url": fake.image_url(),
        "status": "completed",
        "is_featured": True,
        "order": 0,
    }


@pytest.fixture
def sample_achievement_data(fake) -> dict:
    """Generate sample achievement data."""
    return {
        "title": "Hackathon Winner",
        "issuer": fake.company(),
        "date": "2024-03",
        "description": fake.text(max_nb_chars=200),
        "icon": "trophy-icon",
        "order": 0,
    }


@pytest.fixture
def sample_contact_message_data(fake) -> dict:
    """Generate sample contact message data."""
    return {
        "name": fake.name(),
        "email": fake.email(),
        "subject": fake.sentence(),
        "message": fake.text(max_nb_chars=500),
    }


# ============================================================================
# DATABASE FIXTURES - Create persisted data for testing
# ============================================================================

@pytest.fixture
def created_profile(db, sample_profile_data):
    """Create and persist a profile in the test database."""
    profile = Profile(**sample_profile_data)
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


@pytest.fixture
def created_education(db, sample_education_data):
    """Create and persist an education record in the test database."""
    education = Education(**sample_education_data)
    db.add(education)
    db.commit()
    db.refresh(education)
    return education


@pytest.fixture
def created_experience(db, sample_experience_data):
    """Create and persist an experience record in the test database."""
    experience = Experience(**sample_experience_data)
    db.add(experience)
    db.commit()
    db.refresh(experience)
    return experience


@pytest.fixture
def created_skill(db, sample_skill_data):
    """Create and persist a skill in the test database."""
    skill = Skill(**sample_skill_data)
    db.add(skill)
    db.commit()
    db.refresh(skill)
    return skill


@pytest.fixture
def created_certification(db, sample_certification_data):
    """Create and persist a certification in the test database."""
    cert = Certification(**sample_certification_data)
    db.add(cert)
    db.commit()
    db.refresh(cert)
    return cert


@pytest.fixture
def created_project(db, sample_project_data):
    """Create and persist a project in the test database."""
    project = Project(**sample_project_data)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@pytest.fixture
def created_achievement(db, sample_achievement_data):
    """Create and persist an achievement in the test database."""
    achievement = Achievement(**sample_achievement_data)
    db.add(achievement)
    db.commit()
    db.refresh(achievement)
    return achievement


@pytest.fixture
def created_contact_message(db, sample_contact_message_data):
    """Create and persist a contact message in the test database."""
    message = ContactMessage(**sample_contact_message_data)
    db.add(message)
    db.commit()
    db.refresh(message)
    return message
