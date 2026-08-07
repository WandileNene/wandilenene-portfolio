"""
Creates a sample PDF resume and uploads it to the database.
Run: python create_sample_resume.py
"""
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from pathlib import Path
import shutil
from datetime import datetime

from app.database import SessionLocal
from app.models import Resume

# Create a simple PDF resume
def create_sample_pdf():
    """Create a sample resume PDF using ReportLab."""
    filename = "Wandile_Nene_Resume_Sample.pdf"
    filepath = Path("uploads/resumes") / filename
    
    # Ensure directory exists
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    c = canvas.Canvas(str(filepath), pagesize=letter)
    width, height = letter
    
    # Title
    c.setFont("Helvetica-Bold", 24)
    c.drawString(1*inch, height - 1*inch, "WANDILE NENE")
    
    # Contact Info
    c.setFont("Helvetica", 11)
    c.drawString(1*inch, height - 1.3*inch, "Computer Science Graduate & AI Engineer Intern")
    c.drawString(1*inch, height - 1.5*inch, "Email: wandile.nene@example.com | Phone: +27 000 000 0000")
    c.drawString(1*inch, height - 1.7*inch, "GitHub: github.com/wandilenene | LinkedIn: linkedin.com/in/wandilenene")
    
    # Professional Summary
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1*inch, height - 2.2*inch, "PROFESSIONAL SUMMARY")
    c.setFont("Helvetica", 10)
    text = c.beginText(1*inch, height - 2.5*inch)
    text.setFont("Helvetica", 10)
    text.setLeading(14)
    text.textLines("""
Passionate Computer Science graduate and AI Engineer Intern with strong foundation in
software development, machine learning, and AI-driven applications. Proven ability to deliver
scalable and maintainable solutions at the intersection of engineering and AI.
    """)
    c.drawText(text)
    
    # Education
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1*inch, height - 3.5*inch, "EDUCATION")
    c.setFont("Helvetica-Bold", 11)
    c.drawString(1*inch, height - 3.8*inch, "Bachelor of Science in Computer Science")
    c.setFont("Helvetica", 10)
    c.drawString(1*inch, height - 4.0*inch, "University of South Africa (UNISA) | 2020 - 2024 | Pass with Distinction")
    
    # Experience
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1*inch, height - 4.6*inch, "PROFESSIONAL EXPERIENCE")
    
    c.setFont("Helvetica-Bold", 11)
    c.drawString(1*inch, height - 4.9*inch, "AI Engineer Intern")
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(1*inch, height - 5.1*inch, "Tech Company (AI Division) | January 2024 - Present")
    c.setFont("Helvetica", 9)
    text2 = c.beginText(1.2*inch, height - 5.4*inch)
    text2.setFont("Helvetica", 9)
    text2.setLeading(12)
    text2.textLines("""
• Design and implement AI pipelines using Python and modern ML frameworks
• Integrate large language models (LLMs) into production-ready applications
• Evaluate and benchmark model performance across diverse datasets
    """)
    c.drawText(text2)
    
    c.setFont("Helvetica-Bold", 11)
    c.drawString(1*inch, height - 6.3*inch, "Computer Science Tutor")
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(1*inch, height - 6.5*inch, "University / Self-Employed | January 2022 - December 2024")
    c.setFont("Helvetica", 9)
    text3 = c.beginText(1.2*inch, height - 6.8*inch)
    text3.setFont("Helvetica", 9)
    text3.setLeading(12)
    text3.textLines("""
• Tutored students in Python, Java, and data structures
• Created study guides and practice problems for exam preparation
    """)
    c.drawText(text3)
    
    # Skills
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1*inch, height - 7.6*inch, "TECHNICAL SKILLS")
    c.setFont("Helvetica", 10)
    c.drawString(1*inch, height - 7.9*inch, "Languages: Python, JavaScript, TypeScript, Java, C#, SQL")
    c.drawString(1*inch, height - 8.1*inch, "Frameworks: FastAPI, React, Node.js, Next.js, ASP.NET")
    c.drawString(1*inch, height - 8.3*inch, "AI/ML: LangChain, OpenAI API, Scikit-learn, TensorFlow")
    c.drawString(1*inch, height - 8.5*inch, "Tools: Git, Docker, GitHub Actions, Linux, PostgreSQL, MongoDB")
    
    # Certifications
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1*inch, height - 9.1*inch, "CERTIFICATIONS")
    c.setFont("Helvetica", 10)
    c.drawString(1*inch, height - 9.4*inch, "• AI Engineer Professional Certificate - Coursera / deeplearning.ai (2024)")
    c.drawString(1*inch, height - 9.6*inch, "• Python for Data Science and Machine Learning - Udemy (2023)")
    c.drawString(1*inch, height - 9.8*inch, "• Full Stack Web Development Bootcamp (2022)")
    
    # Footer
    c.setFont("Helvetica-Oblique", 8)
    c.drawString(1*inch, 0.5*inch, "This is a sample resume generated for Portfolio API demonstration purposes.")
    
    c.save()
    return filepath, filename


def upload_to_database(filepath, filename):
    """Upload the resume to the database."""
    db = SessionLocal()
    try:
        # Deactivate any existing resumes
        db.query(Resume).update({"is_active": False})
        
        # Create new resume entry
        resume = Resume(
            filename=filename,
            original_filename=filename,
            file_path=str(filepath),
            file_size=filepath.stat().st_size,
            content_type="application/pdf",
            version="v2024.08",
            description="Sample resume for Wandile Nene - AI Engineer & CS Graduate",
            is_active=True,
        )
        db.add(resume)
        db.commit()
        print(f"✅ Sample resume created and uploaded successfully!")
        print(f"   File: {filepath}")
        print(f"   Size: {filepath.stat().st_size} bytes")
        print(f"   Test download: http://localhost:8000/api/v1/resume/download")
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    try:
        from reportlab.pdfgen import canvas as _
    except ImportError:
        print("Installing reportlab...")
        import subprocess
        subprocess.check_call(["pip", "install", "reportlab"])
        print("reportlab installed. Rerun this script.")
        exit(0)
    
    filepath, filename = create_sample_pdf()
    upload_to_database(filepath, filename)
