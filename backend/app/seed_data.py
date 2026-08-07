"""
Seed data for Wandile Nene's portfolio.
This file populates the database with initial portfolio content.
Run with: python -m app.seed_data (from the backend/ directory)
"""

from app.database import SessionLocal, engine
from app import models
from app.models import (
    Profile, Education, Experience, Skill,
    Certification, Project, Achievement
)


def seed_database():
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # -----------------------------------------------
        # Only seed if the DB is empty
        # -----------------------------------------------
        if db.query(Profile).count() > 0:
            print("Database already seeded. Skipping.")
            return

        print("Seeding database with Wandile Nene portfolio data...")

        # -----------------------------------------------
        # Profile
        # -----------------------------------------------
        profile = Profile(
            full_name="Wandile Siphephelo Nene",
            title="Computer Science Graduate & AI Engineer Intern",
            tagline="Building intelligent solutions at the intersection of Software Engineering and Artificial Intelligence.",
            bio=(
                "Computer Science and Information Technology graduate with a strong foundation in software engineering, object-oriented "
                "programming, web development, and database systems. Currently completing an AI Engineer Internship at Indsafri, where I "
                "am building AI-powered applications using Python, FastAPI, REST APIs, Git, and modern software development practices. "
                "Passionate about solving real-world problems, learning new technologies, and collaborating within development teams. "
                "Seeking an opportunity to grow as a software developer where I can contribute while continuously expanding my technical skills."
            ),
            profile_image="/assets/images/profile.jpg",
            email="nenewandile517@gmail.com",
            phone="0724565956",
            location="1 Jager Street Mimosa Square Hillbrow Johannesburg 2001",
            github_url="https://github.com/wandilenene",
            linkedin_url="https://www.linkedin.com/in/wandie-nene-7384642b0",
            twitter_url=None,
        )
        db.add(profile)

        # -----------------------------------------------
        # Education
        # -----------------------------------------------
        education_records = [
            Education(
                degree="Bachelor of Science",
                field_of_study="Computer Science and Information Technology",
                institution="University Of Kwazulu-Natal",
                location="South Africa",
                start_date="2020",
                end_date="2025",
                grade="Degree Completed",
                description=(
                    "Completed a comprehensive degree covering software engineering, "
                    "object-oriented programming, data structures, algorithms, web development, "
                    "database systems, and modern software development practices."
                ),
                is_current=False,
                order=0,
            ),
            Education(
                degree="National Senior Certificate",
                field_of_study="Matric",
                institution="Zindlalele Secondary School",
                location="South Africa",
                start_date="2017",
                end_date="2022",
                grade="Matric Pass",
                description="National Senior Certificate - Matric Pass",
                is_current=False,
                order=1,
            ),
        ]
        db.add_all(education_records)

        # -----------------------------------------------
        # Experience
        # -----------------------------------------------
        experience_records = [
            Experience(
                title="AI Engineer Intern",
                company="Indsafri",
                location="South Africa",
                employment_type="Internship",
                start_date="July 2026",
                end_date=None,
                is_current=True,
                description=(
                    "Building AI-powered applications using Python, FastAPI, REST APIs, Git, and modern "
                    "software development practices. Gaining practical experience with modern AI technologies "
                    "and software engineering workflows."
                ),
                responsibilities=[
                    "Build AI-powered applications using Python and FastAPI",
                    "Develop and consume REST APIs",
                    "Work with Git and GitHub for version control and collaborative development",
                    "Apply prompt engineering techniques to build AI-assisted solutions",
                    "Test, debug and improve backend applications",
                    "Collaborate with mentors and developers while following software development best practices",
                    "Gain practical experience with modern AI technologies and software engineering workflows",
                ],
                technologies=["Python", "FastAPI", "REST APIs", "Git", "GitHub", "AI", "Prompt Engineering"],
                order=0,
            ),
            Experience(
                title="Tutor - COMP200 (Object Oriented Programming) & COMP201 (Data Structures)",
                company="University Of Kwazulu-Natal",
                location="South Africa",
                employment_type="Part-time",
                start_date="February 2025",
                end_date="October 2025",
                is_current=False,
                description=(
                    "Assisted with student academic support and coordination for classes of over 100 students. "
                    "Maintained communication with students regarding coursework and academic progress."
                ),
                responsibilities=[
                    "Assisted with student academic support and coordination for classes of over 100 students",
                    "Maintained communication with students regarding coursework and academic progress",
                    "Helped organise learning materials and academic activities",
                    "Supported administrative and reporting requirements for tutorial sessions",
                ],
                technologies=["Object-Oriented Programming", "Data Structures", "Teaching", "Academic Support"],
                order=1,
            ),
            Experience(
                title="Supplemental Instruction (SI) Leader - STAT130 (Introduction to Statistics)",
                company="University Of Kwazulu-Natal",
                location="South Africa",
                employment_type="Part-time",
                start_date="August 2025",
                end_date="November 2025",
                is_current=False,
                description=(
                    "Coordinated weekly academic support sessions and managed attendance records. "
                    "Prepared learning materials and organised revision activities."
                ),
                responsibilities=[
                    "Coordinated weekly academic support sessions and managed attendance records",
                    "Prepared learning materials and organised revision activities",
                    "Assisted students with academic planning and study support",
                    "Collaborated with lecturers and academic staff to support course objectives",
                ],
                technologies=["Statistics", "Teaching", "Academic Support", "Student Mentoring"],
                order=2,
            ),
        ]
        db.add_all(experience_records)

        # -----------------------------------------------
        # Skills
        # -----------------------------------------------
        skills = [
            # Programming Languages
            Skill(name="C#", category="Languages", proficiency=85, icon="csharp", order=0),
            Skill(name="Java", category="Languages", proficiency=82, icon="java", order=1),
            Skill(name="JavaScript", category="Languages", proficiency=80, icon="javascript", order=2),
            Skill(name="C++", category="Languages", proficiency=78, icon="cpp", order=3),
            Skill(name="Python", category="Languages", proficiency=90, icon="python", order=4),
            Skill(name="SQL", category="Languages", proficiency=85, icon="sql", order=5),
            # Backend
            Skill(name="FastAPI", category="Backend", proficiency=88, icon="fastapi", order=0),
            Skill(name="ASP.NET", category="Backend", proficiency=80, icon="dotnet", order=1),
            Skill(name=".NET Framework", category="Backend", proficiency=78, icon="dotnet", order=2),
            Skill(name="REST APIs", category="Backend", proficiency=85, icon="api", order=3),
            # Frontend
            Skill(name="HTML5", category="Frontend", proficiency=88, icon="html5", order=0),
            Skill(name="CSS3", category="Frontend", proficiency=85, icon="css3", order=1),
            Skill(name="JavaScript", category="Frontend", proficiency=80, icon="javascript", order=2),
            # Database
            Skill(name="SQL Server", category="Database", proficiency=85, icon="sqlserver", order=0),
            Skill(name="MySQL", category="Database", proficiency=82, icon="mysql", order=1),
            Skill(name="Database Design", category="Database", proficiency=80, icon="database", order=2),
            # Software Engineering
            Skill(name="Object-Oriented Programming (OOP)", category="Software Engineering", proficiency=90, icon="oop", order=0),
            Skill(name="Git & GitHub", category="Software Engineering", proficiency=88, icon="git", order=1),
            Skill(name="MVC Architecture", category="Software Engineering", proficiency=82, icon="architecture", order=2),
            Skill(name="CRUD Operations", category="Software Engineering", proficiency=85, icon="crud", order=3),
            Skill(name="Authentication & Authorization", category="Software Engineering", proficiency=80, icon="security", order=4),
            Skill(name="SDLC", category="Software Engineering", proficiency=78, icon="sdlc", order=5),
            Skill(name="Debugging & Testing", category="Software Engineering", proficiency=82, icon="testing", order=6),
            # AI & Machine Learning
            Skill(name="Prompt Engineering", category="AI & Machine Learning", proficiency=85, icon="ai", order=0),
            Skill(name="Large Language Models (LLMs)", category="AI & Machine Learning", proficiency=80, icon="llm", order=1),
            Skill(name="AI Application Development", category="AI & Machine Learning", proficiency=82, icon="ai-app", order=2),
            Skill(name="API Integration", category="AI & Machine Learning", proficiency=85, icon="integration", order=3),
            # Tools & Platforms
            Skill(name="Visual Studio", category="Tools & Platforms", proficiency=85, icon="visualstudio", order=0),
            Skill(name="VS Code", category="Tools & Platforms", proficiency=90, icon="vscode", order=1),
            Skill(name="Git", category="Tools & Platforms", proficiency=88, icon="git", order=2),
            Skill(name="GitHub", category="Tools & Platforms", proficiency=88, icon="github", order=3),
            Skill(name="Microsoft Azure", category="Tools & Platforms", proficiency=75, icon="azure", order=4),
            Skill(name="Microsoft Word", category="Tools & Platforms", proficiency=85, icon="word", order=5),
            Skill(name="Microsoft Excel", category="Tools & Platforms", proficiency=82, icon="excel", order=6),
            Skill(name="Microsoft PowerPoint", category="Tools & Platforms", proficiency=80, icon="powerpoint", order=7),
        ]
        db.add_all(skills)

        # -----------------------------------------------
        # Certifications
        # -----------------------------------------------
        certifications = [
            # Add certifications here when available
        ]
        if certifications:
            db.add_all(certifications)

        # -----------------------------------------------
        # Projects
        # -----------------------------------------------
        projects = [
            Project(
                name="AI Calculator API",
                slug="ai-calculator-api",
                short_description="A calculator web application built with FastAPI and JavaScript.",
                description=(
                    "Built a fully functional calculator web application using FastAPI for the backend and JavaScript for the frontend. "
                    "The project demonstrates REST API development, asynchronous JavaScript operations, and full-stack integration. "
                    "Features comprehensive API endpoints for arithmetic operations with proper error handling and testing."
                ),
                technologies=["Python", "FastAPI", "HTML", "CSS", "JavaScript"],
                features=[
                    "Built a calculator web application using FastAPI and JavaScript",
                    "Developed REST API endpoints for arithmetic operations",
                    "Connected frontend and backend using asynchronous JavaScript",
                    "Tested API endpoints and debugged application errors",
                    "Managed the project using Git and GitHub",
                ],
                github_url="https://github.com/wandilenene/ai-calculator-api",
                demo_url=None,
                image_url="/assets/images/projects/calculator.jpg",
                status="completed",
                is_featured=True,
                order=0,
            ),
            Project(
                name="Echoes Of Death - Quiz Game",
                slug="echoes-of-death",
                short_description="A 3-level story driven quiz game developed as a final-year project.",
                description=(
                    "A 3-level story driven quiz game developed as a final-year project using C++ and SFML. "
                    "Each level tests players through engaging question rounds and interactive sub-games. "
                    "The project showcases advanced game development concepts including game architecture, "
                    "rendering pipelines, animations, and state management."
                ),
                technologies=["C++", "SFML"],
                features=[
                    "3-level story driven gameplay with progressive difficulty",
                    "Co-developed the game architecture using C++ and SFML",
                    "Led development of game logic, rendering, animations, and level transitions",
                    "Integrated player progress tracking and scoring system",
                    "Interactive sub-games and engaging question rounds",
                ],
                github_url="https://github.com/wandilenene/echoes-of-death",
                demo_url=None,
                image_url="/assets/images/projects/quiz-game.jpg",
                status="completed",
                is_featured=True,
                order=1,
            ),
            Project(
                name="Software Development Project - University Group Project",
                slug="software-development-project",
                short_description="A comprehensive full-stack web application developed as a 3rd year university group project.",
                description=(
                    "Participated in a structured software development project following industry best practices. "
                    "The team developed a full-stack web application using C#, ASP.NET, SQL Server, and modern web technologies. "
                    "The project involved requirements gathering, database design, backend development, frontend implementation, "
                    "and deployment to Microsoft Azure."
                ),
                technologies=["C#", "SQL Server", "HTML", "JavaScript", "GitHub", "Microsoft Azure", "Visual Studio", "ASP.NET"],
                features=[
                    "Participated in requirements gathering and client meetings to analyse business needs",
                    "Developed front-end interfaces and backend business logic using HTML, Javascript, C# and ASP.NET",
                    "Designed and implemented relational databases using SQL Server",
                    "Built CRUD functionalities, authentication systems, and reporting features",
                    "Worked with REST-style APIs and integrated backend data operations",
                    "Used Git for version control and collaborative development",
                    "Assisted with deploying and publishing the web application using Microsoft Azure",
                    "Followed structured software development and team collaboration practices",
                ],
                github_url=None,
                demo_url=None,
                image_url="/assets/images/projects/university-project.jpg",
                status="completed",
                is_featured=False,
                order=2,
            ),
            Project(
                name="Survey Management Web Application",
                slug="survey-management",
                short_description="A full-stack web application for managing surveys with authentication and role-based access control.",
                description=(
                    "Designed and developed a comprehensive full-stack web application using ASP.NET, C#, HTML, JavaScript, and SQL Server. "
                    "The application features complete survey management capabilities with authentication, role-based access control, "
                    "and a well-structured database design following MVC principles."
                ),
                technologies=["ASP.NET", "C#", "HTML", "JavaScript", "SQL Server", "Git"],
                features=[
                    "Implemented authentication and role-based access control",
                    "Built REST-style backend logic with CRUD operations",
                    "Designed relational database schema and optimized queries",
                    "Collaborated using Git version control",
                    "Applied MVC principles and structured development practices",
                ],
                github_url=None,
                demo_url=None,
                image_url="/assets/images/projects/survey-app.jpg",
                status="completed",
                is_featured=False,
                order=3,
            ),
        ]
        db.add_all(projects)

        # -----------------------------------------------
        # Achievements
        # -----------------------------------------------
        achievements = [
            Achievement(
                title="Tutor - COMP200 & COMP201",
                issuer="University Of Kwazulu-Natal",
                date="2025",
                description=(
                    "Selected to tutor Object-Oriented Programming and Data Structures, "
                    "providing academic support and coordination for classes of over 100 students."
                ),
                icon="award",
                order=0,
            ),
            Achievement(
                title="Supplemental Instruction (SI) Leader - STAT130",
                issuer="University Of Kwazulu-Natal",
                date="2025",
                description=(
                    "Appointed as SI Leader for Introduction to Statistics, coordinating weekly "
                    "academic support sessions, managing attendance records, and collaborating "
                    "with lecturers to support course objectives."
                ),
                icon="star",
                order=1,
            ),
            Achievement(
                title="BSc Computer Science and Information Technology - Degree Completed",
                issuer="University Of Kwazulu-Natal",
                date="2025",
                description=(
                    "Successfully completed a Bachelor of Science degree in Computer Science and "
                    "Information Technology, building a strong foundation in software engineering, "
                    "OOP, web development, and database systems."
                ),
                icon="graduation",
                order=2,
            ),
            Achievement(
                title="AI Engineer Internship",
                issuer="Indsafri",
                date="2026",
                description=(
                    "Selected for an AI Engineer Internship at Indsafri, building AI-powered "
                    "applications using Python, FastAPI, REST APIs, and applying prompt engineering "
                    "techniques to develop AI-assisted solutions."
                ),
                icon="trophy",
                order=3,
            ),
        ]
        db.add_all(achievements)

        db.commit()
        print("✅ Database seeded successfully with Wandile Nene portfolio data.")

    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
