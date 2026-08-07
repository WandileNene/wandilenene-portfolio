from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError
import time

from app.config import settings
from app.database import engine
from app import models

from app.routers import (
    profile,
    education,
    experience,
    skills,
    certifications,
    projects,
    achievements,
    contact,
    resume,
    summary,
)

# -------------------------------------------------------
# Create all tables on startup
# -------------------------------------------------------
models.Base.metadata.create_all(bind=engine)

# -------------------------------------------------------
# Application Instance
# -------------------------------------------------------
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "REST API for Wandile Nene's Portfolio Website.\n\n"
        "This API serves all portfolio content including profile, education, "
        "experience, skills, certifications, projects, achievements, and contact messages.\n\n"
        "Use `GET /api/v1/summary` for a single consolidated response of all portfolio data."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# -------------------------------------------------------
# CORS Middleware
# -------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------------
# Request Timing Middleware
# -------------------------------------------------------
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = f"{process_time:.4f}s"
    return response

# -------------------------------------------------------
# Global Exception Handlers
# -------------------------------------------------------
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        errors.append({
            "field": " -> ".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"],
        })
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation Error",
            "detail": "One or more fields failed validation.",
            "errors": errors,
        },
    )


@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    return JSONResponse(
        status_code=409,
        content={
            "error": "Conflict",
            "detail": "A database integrity constraint was violated. Possible duplicate entry.",
        },
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "detail": str(exc) if settings.debug else "An unexpected error occurred.",
        },
    )

# -------------------------------------------------------
# Include Routers (all under /api/v1 prefix)
# -------------------------------------------------------
API_PREFIX = "/api/v1"

app.include_router(profile.router, prefix=API_PREFIX)
app.include_router(education.router, prefix=API_PREFIX)
app.include_router(experience.router, prefix=API_PREFIX)
app.include_router(skills.router, prefix=API_PREFIX)
app.include_router(certifications.router, prefix=API_PREFIX)
app.include_router(projects.router, prefix=API_PREFIX)
app.include_router(achievements.router, prefix=API_PREFIX)
app.include_router(contact.router, prefix=API_PREFIX)
app.include_router(resume.router, prefix=API_PREFIX)
app.include_router(summary.router, prefix=API_PREFIX)

# -------------------------------------------------------
# Root & Health Check Endpoints
# -------------------------------------------------------
@app.get("/", tags=["Health"])
def root():
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "running",
        "environment": settings.environment,
        "docs": "/docs",
        "redoc": "/redoc",
        "api_prefix": API_PREFIX,
    }


@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "version": settings.app_version,
        "environment": settings.environment,
    }
