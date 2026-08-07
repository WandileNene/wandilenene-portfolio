# Portfolio API — Backend

FastAPI-based REST API serving Wandile Nene's portfolio content.

## Features

- ✅ **Complete CRUD** for all portfolio sections
- ✅ **Resume Management** — Upload, download, and version control
- ✅ **Auto-generated API Docs** (Swagger UI + ReDoc)
- ✅ **Input Validation** with Pydantic v2
- ✅ **CORS-enabled** for frontend integration
- ✅ **SQLite** persistence (easily swappable for PostgreSQL)
- ✅ **Seed Data** for instant setup

---

## Quick Start

### 1. Install Dependencies

```powershell
cd backend
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Seed Database

```powershell
python -m app.seed_data
```

### 3. Run Server

```powershell
python run.py
```

Server starts at: **`http://localhost:8000`**

---

## API Endpoints

### Core Endpoints

| Endpoint | Description |
|---|---|
| `GET /` | API info and status |
| `GET /health` | Health check |
| `GET /docs` | Swagger UI (interactive docs) |
| `GET /redoc` | ReDoc (clean API reference) |
| `GET /api/v1/summary/` | **Full portfolio in one JSON response** |

### Resource Endpoints

| Resource | Endpoints |
|---|---|
| **Profile** | `GET`, `POST`, `PATCH`, `DELETE /api/v1/profile/` |
| **Education** | `GET`, `POST /api/v1/education/` <br> `GET`, `PATCH`, `DELETE /api/v1/education/{id}` |
| **Experience** | `GET`, `POST /api/v1/experience/` <br> `GET`, `PATCH`, `DELETE /api/v1/experience/{id}` |
| **Skills** | `GET`, `POST /api/v1/skills/` <br> `GET /api/v1/skills/grouped` <br> `GET`, `PATCH`, `DELETE /api/v1/skills/{id}` |
| **Certifications** | `GET`, `POST /api/v1/certifications/` <br> `GET`, `PATCH`, `DELETE /api/v1/certifications/{id}` |
| **Projects** | `GET`, `POST /api/v1/projects/` <br> `GET /api/v1/projects/featured` <br> `GET /api/v1/projects/slug/{slug}` <br> `GET`, `PATCH`, `DELETE /api/v1/projects/{id}` |
| **Achievements** | `GET`, `POST /api/v1/achievements/` <br> `GET`, `PATCH`, `DELETE /api/v1/achievements/{id}` |
| **Contact** | `POST /api/v1/contact/` <br> `GET /api/v1/contact/messages` <br> `PATCH /api/v1/contact/messages/{id}/read` |
| **Resume** | `GET /api/v1/resume/` (metadata) <br> `GET /api/v1/resume/download` (file download) <br> `POST /api/v1/resume/upload` (file upload) <br> `GET /api/v1/resume/all` (all versions) <br> `PATCH /api/v1/resume/{id}/activate` |

---

## Testing with Postman

1. Import `postman_collection.json` into Postman
2. Verify `baseUrl` variable = `http://localhost:8000`
3. Follow `TESTING_GUIDE.md` for phase-by-phase testing

---

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app
│   ├── config.py            # Settings
│   ├── database.py          # SQLAlchemy setup
│   ├── models.py            # Database models
│   ├── schemas.py           # Pydantic schemas
│   ├── seed_data.py         # Seed script
│   └── routers/             # API endpoints
│       ├── profile.py
│       ├── education.py
│       ├── experience.py
│       ├── skills.py
│       ├── certifications.py
│       ├── projects.py
│       ├── achievements.py
│       ├── contact.py
│       ├── resume.py
│       └── summary.py
├── uploads/resumes/         # Resume file storage
├── requirements.txt
├── run.py                   # Server entry point
├── .env                     # Environment config
├── portfolio.db             # SQLite database
├── postman_collection.json  # Postman collection
├── TESTING_GUIDE.md         # Complete testing guide
└── README.md                # This file
```

---

## Environment Variables

Edit `.env` to configure:

```env
APP_NAME="Portfolio API"
APP_VERSION="1.0.0"
DEBUG=True
ENVIRONMENT=development

HOST=0.0.0.0
PORT=8000

CORS_ORIGINS=http://localhost:3000,http://localhost:5173
DATABASE_URL=sqlite:///./portfolio.db

SECRET_KEY=your-secret-key-change-in-production
```

---

## Resume Management

### Upload Resume

```bash
POST /api/v1/resume/upload
Content-Type: multipart/form-data

file: [PDF or DOCX file]
version: "v2024.08" (optional)
description: "Latest resume" (optional)
```

### Download Resume

```bash
GET /api/v1/resume/download
```

Returns the currently active resume file.

### View Metadata

```bash
GET /api/v1/resume/
```

Returns metadata (filename, size, version) without downloading the file.

---

## Deployment

### Option 1: Railway / Render

1. Push code to GitHub
2. Connect to Railway/Render
3. Set environment variables
4. Deploy

### Option 2: Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "run.py"]
```

### Option 3: Azure / AWS

Use App Service (Azure) or Elastic Beanstalk (AWS) with Python runtime.

---

## Tech Stack

- **Framework**: FastAPI 0.141+
- **ORM**: SQLAlchemy 2.0+
- **Validation**: Pydantic 2.13+
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **Server**: Uvicorn with auto-reload

---

## Next Steps

1. ✅ Backend API fully implemented
2. ⬜ Build React frontend
3. ⬜ Connect frontend to backend via `/api/v1/summary/`
4. ⬜ Deploy to production
5. ⬜ Add authentication for admin routes (optional)

---

**Built with FastAPI by Wandile Nene** 🚀
