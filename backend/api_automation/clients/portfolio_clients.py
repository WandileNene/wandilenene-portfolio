"""
Portfolio API Clients
Specialized API clients for different portfolio endpoints.
"""

from typing import Dict, Any, Optional, List
from api_automation.clients.base_client import BaseAPIClient, APIResponse


class ProfileClient(BaseAPIClient):
    """Client for Profile API endpoints."""
    
    def get_profile(self) -> APIResponse:
        """Get user profile."""
        return self.get("/profile")
    
    def create_profile(self, payload: Dict[str, Any]) -> APIResponse:
        """Create a new profile."""
        return self.post("/profile", json=payload)
    
    def update_profile(self, payload: Dict[str, Any]) -> APIResponse:
        """Update user profile."""
        return self.patch("/profile", json=payload)
    
    def delete_profile(self) -> APIResponse:
        """Delete user profile."""
        return self.delete("/profile")


class EducationClient(BaseAPIClient):
    """Client for Education API endpoints."""
    
    def get_all_education(self) -> APIResponse:
        """Get all education records."""
        return self.get("/education")
    
    def get_education(self, education_id: int) -> APIResponse:
        """Get a specific education record."""
        return self.get(f"/education/{education_id}")
    
    def create_education(self, payload: Dict[str, Any]) -> APIResponse:
        """Create a new education record."""
        return self.post("/education", json=payload)
    
    def update_education(self, education_id: int, payload: Dict[str, Any]) -> APIResponse:
        """Update an education record."""
        return self.patch(f"/education/{education_id}", json=payload)
    
    def delete_education(self, education_id: int) -> APIResponse:
        """Delete an education record."""
        return self.delete(f"/education/{education_id}")


class ExperienceClient(BaseAPIClient):
    """Client for Experience API endpoints."""
    
    def get_all_experience(self, include_current: bool = True) -> APIResponse:
        """Get all experience records."""
        params = {"include_current": str(include_current).lower()}
        return self.get("/experience", params=params)
    
    def get_experience(self, experience_id: int) -> APIResponse:
        """Get a specific experience record."""
        return self.get(f"/experience/{experience_id}")
    
    def create_experience(self, payload: Dict[str, Any]) -> APIResponse:
        """Create a new experience record."""
        return self.post("/experience", json=payload)
    
    def update_experience(self, experience_id: int, payload: Dict[str, Any]) -> APIResponse:
        """Update an experience record."""
        return self.patch(f"/experience/{experience_id}", json=payload)
    
    def delete_experience(self, experience_id: int) -> APIResponse:
        """Delete an experience record."""
        return self.delete(f"/experience/{experience_id}")


class SkillClient(BaseAPIClient):
    """Client for Skills API endpoints."""
    
    def get_all_skills(self, category: Optional[str] = None) -> APIResponse:
        """Get all skills, optionally filtered by category."""
        params = {}
        if category:
            params["category"] = category
        return self.get("/skills", params=params if params else None)
    
    def get_skills_grouped(self) -> APIResponse:
        """Get skills grouped by category."""
        return self.get("/skills/grouped")
    
    def get_skill_categories(self) -> APIResponse:
        """Get all skill categories."""
        return self.get("/skills/categories")
    
    def get_skill(self, skill_id: int) -> APIResponse:
        """Get a specific skill."""
        return self.get(f"/skills/{skill_id}")
    
    def create_skill(self, payload: Dict[str, Any]) -> APIResponse:
        """Create a new skill."""
        return self.post("/skills", json=payload)
    
    def update_skill(self, skill_id: int, payload: Dict[str, Any]) -> APIResponse:
        """Update a skill."""
        return self.patch(f"/skills/{skill_id}", json=payload)
    
    def delete_skill(self, skill_id: int) -> APIResponse:
        """Delete a skill."""
        return self.delete(f"/skills/{skill_id}")


class ProjectClient(BaseAPIClient):
    """Client for Projects API endpoints."""
    
    def get_all_projects(self, featured_only: bool = False) -> APIResponse:
        """Get all projects."""
        params = {}
        if featured_only:
            params["featured_only"] = "true"
        return self.get("/projects", params=params if params else None)
    
    def get_featured_projects(self) -> APIResponse:
        """Get featured projects only."""
        return self.get("/projects/featured")
    
    def get_project_by_slug(self, slug: str) -> APIResponse:
        """Get project by slug."""
        return self.get(f"/projects/by-slug/{slug}")
    
    def get_project(self, project_id: int) -> APIResponse:
        """Get a specific project."""
        return self.get(f"/projects/{project_id}")
    
    def create_project(self, payload: Dict[str, Any]) -> APIResponse:
        """Create a new project."""
        return self.post("/projects", json=payload)
    
    def update_project(self, project_id: int, payload: Dict[str, Any]) -> APIResponse:
        """Update a project."""
        return self.patch(f"/projects/{project_id}", json=payload)
    
    def delete_project(self, project_id: int) -> APIResponse:
        """Delete a project."""
        return self.delete(f"/projects/{project_id}")


class AchievementClient(BaseAPIClient):
    """Client for Achievements API endpoints."""
    
    def get_all_achievements(self) -> APIResponse:
        """Get all achievements."""
        return self.get("/achievements")
    
    def get_achievement(self, achievement_id: int) -> APIResponse:
        """Get a specific achievement."""
        return self.get(f"/achievements/{achievement_id}")
    
    def create_achievement(self, payload: Dict[str, Any]) -> APIResponse:
        """Create a new achievement."""
        return self.post("/achievements", json=payload)
    
    def update_achievement(self, achievement_id: int, payload: Dict[str, Any]) -> APIResponse:
        """Update an achievement."""
        return self.patch(f"/achievements/{achievement_id}", json=payload)
    
    def delete_achievement(self, achievement_id: int) -> APIResponse:
        """Delete an achievement."""
        return self.delete(f"/achievements/{achievement_id}")


class CertificationClient(BaseAPIClient):
    """Client for Certifications API endpoints."""
    
    def get_all_certifications(self) -> APIResponse:
        """Get all certifications."""
        return self.get("/certifications")
    
    def get_certification(self, cert_id: int) -> APIResponse:
        """Get a specific certification."""
        return self.get(f"/certifications/{cert_id}")
    
    def create_certification(self, payload: Dict[str, Any]) -> APIResponse:
        """Create a new certification."""
        return self.post("/certifications", json=payload)
    
    def update_certification(self, cert_id: int, payload: Dict[str, Any]) -> APIResponse:
        """Update a certification."""
        return self.patch(f"/certifications/{cert_id}", json=payload)
    
    def delete_certification(self, cert_id: int) -> APIResponse:
        """Delete a certification."""
        return self.delete(f"/certifications/{cert_id}")


class ContactClient(BaseAPIClient):
    """Client for Contact API endpoints."""
    
    def send_message(self, payload: Dict[str, Any]) -> APIResponse:
        """Send a contact message."""
        return self.post("/contact", json=payload)
    
    def get_all_messages(self) -> APIResponse:
        """Get all contact messages."""
        return self.get("/contact")
    
    def get_message(self, message_id: int) -> APIResponse:
        """Get a specific contact message."""
        return self.get(f"/contact/{message_id}")
    
    def mark_message_read(self, message_id: int) -> APIResponse:
        """Mark a message as read."""
        return self.patch(f"/contact/{message_id}", json={"is_read": True})
    
    def delete_message(self, message_id: int) -> APIResponse:
        """Delete a contact message."""
        return self.delete(f"/contact/{message_id}")


class SummaryClient(BaseAPIClient):
    """Client for Summary API endpoint (consolidated portfolio data)."""
    
    def get_portfolio_summary(self) -> APIResponse:
        """Get consolidated portfolio summary."""
        return self.get("/summary")
