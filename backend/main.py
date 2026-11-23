# Entry point for Render deployment.
# Render runs `uvicorn main:app` from this directory,
# so we re-export the app from the actual module location.
from app.main import app  # noqa: F401
