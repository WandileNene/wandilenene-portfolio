# Wandile Nene — Portfolio Website

Complete full-stack portfolio website with FastAPI backend and React frontend.

---

## 🎯 Project Overview

A modern, responsive portfolio website showcasing:
- Professional profile and bio
- Education history
- Work experience timeline
- Technical skills (23 skills in 5 categories)
- Portfolio projects (4 featured projects)
- Certifications and achievements
- Downloadable resume
- Contact form integration

**Stack:**
- **Backend:** Python, FastAPI, SQLAlchemy, SQLite
- **Frontend:** React, TypeScript, Vite
- **Architecture:** REST API with single-endpoint summary for optimal performance

---

## 🚀 Quick Start

### Option 1: One-Command Start (Recommended)

**Terminal 1 - Backend:**
```powershell
cd backend
.\venv\Scripts\python.exe run.py
```
Backend runs on `http://localhost:8000`

**Terminal 2 - Frontend:**
```powershell
cd frontend
npm run dev
```
Frontend runs on `http://localhost:5173`

**Then open:** `http://localhost:5173` in your browser

### Option 2: First-Time Setup

See [RUNNING_GUIDE.md](./RUNNING_GUIDE.md) for complete step-by-step instructions.

---

## 📁 Project Structure

```
portfolio_copilot/
├── backend/                    # FastAPI REST API
│   ├── app/
│   │   ├── main.py            # FastAPI app
│   │   ├── models.py          # Database models
│   │   ├── schemas.py         # Pydantic schemas
│   │   ├── database.py        # SQLAlchemy setup
│   │   ├── config.py          # Configuration
│   │   ├── seed_data.py       # Database seeder
│   │   └── routers/           # API endpoints
│   │       ├── profile.py
│   │       ├── education.py
│   │       ├── experience.py
│   │       ├── skills.py
│   │       ├── certifications.py
│   │       ├── projects.py
│   │       ├── achievements.py
│   │       ├── contact.py
│   │       ├── resume.py
│   │       └── summary.py     # ⭐ Main endpoint
│   ├── uploads/resumes/       # Resume file storage
│   ├── requirements.txt
│   ├── run.py
│   ├── .env
│   ├── portfolio.db           # SQLite database
│   ├── postman_collection.json
│   └── TESTING_GUIDE.md
│
├── frontend/                   # React + TypeScript SPA
│   ├── src/
│   │   ├── App.tsx            # Main app component
│   │   ├── main.tsx           # React entry point
│   │   ├── components/        # React components
│   │   │   ├── Navbar/
│   │   │   ├── Hero/
│   │   │   └── shared/
│   │   ├── hooks/             # Custom hooks
│   │   │   ├── usePortfolio.ts
│   │   │   └── useScrollReveal.ts
│   │   ├── services/
│   │   │   └── api.ts         # API client
│   │   ├── types/
│   │   │   └── api.ts         # TypeScript types
│   │   └── styles/
│   │       ├── global.css
│   │       └── variables.css
│   ├── index.html
│   ├── vite.config.ts         # Vite config with proxy
│   ├── package.json
│   └── README.md
│
├── architecture.md             # Complete design specification
├── RUNNING_GUIDE.md           # How to run locally
└── README.md                  # This file
```

---

## 🎨 Design System

Following the architecture.md specifications:

**Colors:**
- Primary: `#0F172A` (Navy blue)
- Secondary: `#1D4ED8` (Royal blue)
- Accent: `#14B8A6` (Teal)
- Background: `#F8FAFC` (Light gray)
- Surface: `#FFFFFF` (White)

**Typography:**
- Headings: Poppins
- Body: Inter
- Display: Space Grotesk

**Features:**
- Responsive design (mobile-first)
- Smooth scroll navigation
- Typing animation in hero
- Scroll reveal animations
- Accessible (WCAG compliant)
- SEO optimized

---

## 🔌 API Endpoints

### Primary Endpoint (Recommended)
- `GET /api/v1/summary/` — Returns complete portfolio in one request

### Resource Endpoints
- `GET /api/v1/profile/` — Profile and about info
- `GET /api/v1/education/` — Education records
- `GET /api/v1/experience/` — Work experience
- `GET /api/v1/skills/grouped` — Skills by category
- `GET /api/v1/certifications/` — Certifications
- `GET /api/v1/projects/` — All projects
- `GET /api/v1/projects/featured` — Featured projects only
- `GET /api/v1/achievements/` — Awards and achievements
- `GET /api/v1/resume/download` — Download active resume
- `POST /api/v1/contact/` — Submit contact form

### API Documentation
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- Postman Collection: `backend/postman_collection.json`

---

## ✅ Features Checklist

### Backend ✅
- [x] Complete REST API with FastAPI
- [x] SQLite database with SQLAlchemy
- [x] Full CRUD for all resources
- [x] Pydantic v2 validation
- [x] Resume upload/download
- [x] Contact form submission
- [x] Auto-generated OpenAPI docs
- [x] CORS configured
- [x] Seed data command
- [x] Error handling
- [x] Postman collection

### Frontend ✅
- [x] React + TypeScript setup
- [x] Vite build tooling
- [x] API integration via usePortfolio hook
- [x] Responsive navbar with mobile menu
- [x] Hero section with typing effect
- [x] All portfolio sections rendering
- [x] Skills grouped by category
- [x] Resume download button
- [x] Smooth scroll navigation
- [x] Loading states
- [x] Error handling
- [x] TypeScript types matching backend schemas

---

## 🧪 Testing

### Backend Testing
```powershell
cd backend
# Test with Postman (import postman_collection.json)
# Or use Swagger UI at http://localhost:8000/docs
```

See [backend/TESTING_GUIDE.md](./backend/TESTING_GUIDE.md) for phase-by-phase testing instructions.

### Frontend Testing
```powershell
cd frontend
npm run dev
# Open http://localhost:5173
```

**Manual Testing Checklist:**
- [ ] Page loads without errors
- [ ] Navbar navigation works
- [ ] Hero displays profile info
- [ ] All sections populated with data
- [ ] Skills show 23 items in 5 categories
- [ ] Projects show 4 projects
- [ ] Resume download works
- [ ] No console errors (F12)

---

## 📊 Current Status

### ✅ Completed
- Backend API fully implemented (10 routers, 50+ endpoints)
- Database seeded with real portfolio data
- Frontend scaffolded with React + TypeScript
- API integration working
- Basic UI components (Navbar, Hero, sections)
- Responsive design system
- Resume upload/download

### 🚧 To Enhance (Optional)
- Full component styling for all sections
- Contact form with validation
- Animations and transitions
- Project detail pages
- Image uploads for projects
- Admin dashboard
- Dark mode toggle
- Blog section

---

## 🚢 Deployment

### Backend Options
- **Railway** — `railway up` (easiest)
- **Render** — Connect GitHub repo
- **AWS/Azure** — Elastic Beanstalk / App Service

### Frontend Options
- **Vercel** — `vercel deploy`
- **Netlify** — Drag-and-drop `dist/` folder after `npm run build`
- **GitHub Pages** — For static build only

### Environment Variables for Production
```env
# Backend
DATABASE_URL=postgresql://...  # Upgrade from SQLite
SECRET_KEY=<strong-random-key>
ENVIRONMENT=production
DEBUG=False
CORS_ORIGINS=https://yourdomain.com

# Frontend
VITE_API_URL=https://your-backend.com
```

---

## 📝 Content Management

### Update Portfolio Data

**Option 1: Via Postman**
- Import `backend/postman_collection.json`
- Use PATCH/POST endpoints to update

**Option 2: Via Swagger UI**
- Open `http://localhost:8000/docs`
- Use interactive forms

**Option 3: Re-seed Database**
- Edit `backend/app/seed_data.py`
- Delete `backend/portfolio.db`
- Run `python -m app.seed_data`

**Option 4: Direct Database**
- Use SQLite browser to edit `portfolio.db`

---

## 🛠️ Technologies

### Backend
- **FastAPI** 0.141+ — Modern Python web framework
- **SQLAlchemy** 2.0+ — ORM
- **Pydantic** 2.13+ — Data validation
- **Uvicorn** — ASGI server
- **SQLite** — Database (easily swappable for PostgreSQL)

### Frontend
- **React** 18.3+ — UI library
- **TypeScript** 5.5+ — Type safety
- **Vite** 5.4+ — Build tool
- **CSS Modules** — Scoped styling

---

## 📚 Documentation

- [architecture.md](./architecture.md) — Complete design specification
- [RUNNING_GUIDE.md](./RUNNING_GUIDE.md) — How to run locally
- [backend/README.md](./backend/README.md) — Backend API docs
- [backend/TESTING_GUIDE.md](./backend/TESTING_GUIDE.md) — API testing guide
- [frontend/README.md](./frontend/README.md) — Frontend docs

---

## 🤝 Contributing

This is a personal portfolio project. To use as a template:

1. Fork the repository
2. Update `backend/app/seed_data.py` with your data
3. Replace profile image in `public/`
4. Update colors in `frontend/src/styles/variables.css` (optional)
5. Deploy!

---

## 📄 License

Personal portfolio project © 2024 Wandile Nene

---

## 🎉 Credits

**Built by:** Wandile Nene  
**Stack:** Python (FastAPI) + React (TypeScript)  
**Architecture:** RESTful API with SPA frontend  
**Status:** Production-ready ✅

---

**For support, check [RUNNING_GUIDE.md](./RUNNING_GUIDE.md) or open an issue.**
