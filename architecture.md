# Portfolio Website Architecture

## 1. Executive Summary

This document defines the architecture for a modern, responsive, full-stack portfolio website for Wandile Nene, a Computer Science graduate and AI Engineer Intern.

The portfolio is implemented as a **React 18 + TypeScript** frontend (with Vite) consuming a **FastAPI** backend API with **SQLite** database storage. It demonstrates proficiency with modern full-stack development including RESTful API design, component-based UI architecture, database modeling, responsive design, and email integration.

**Technology Stack:**
- **Frontend:** React 18 + TypeScript + Vite + CSS Modules
- **Backend:** FastAPI + Python 3.10+ + SQLAlchemy 2.0
- **Database:** SQLite 3.x
- **Features:** Dark/light themes, contact form with email, resume download, smooth navigation

---

## 2. System Architecture Overview

### Three-Tier Architecture

```
┌──────────────────────────────────────────────────┐
│         PRESENTATION TIER                        │
│   React 18 + TypeScript + Vite                  │
│   Port: 5173 (dev)                              │
└─────────────┬────────────────────────────────────┘
              │ HTTP/REST (Fetch API)
┌─────────────▼────────────────────────────────────┐
│         APPLICATION TIER                         │
│   FastAPI + Pydantic + SQLAlchemy               │
│   Port: 8000                                    │
└─────────────┬────────────────────────────────────┘
              │ SQLAlchemy ORM
┌─────────────▼────────────────────────────────────┐
│         DATA TIER                                │
│   SQLite (portfolio.db)                         │
│   10 Tables                                     │
└──────────────────────────────────────────────────┘
```

---

## 3. Frontend Architecture

### Technology Stack

| Layer | Technology | Version |
|-------|------------|---------|
| Framework | React | 18.3.1 |
| Language | TypeScript | 5.5.3 |
| Build Tool | Vite | 5.4.2 |
| Styling | CSS Modules + CSS Variables | Native |
| HTTP Client | Fetch API | Native |

### Folder Structure

```
frontend/
├── public/
│   ├── images/              # Profile photos, assets
│   ├── icons.svg
│   └── favicon.svg
├── src/
│   ├── components/
│   │   ├── Contact/         # Contact form
│   │   ├── Hero/            # Hero section with typing effect
│   │   ├── Navbar/          # Navigation with theme toggle
│   │   └── shared/          # Reusable components
│   ├── context/
│   │   └── ThemeContext.tsx # Theme management
│   ├── hooks/
│   │   ├── usePortfolio.ts  # Data fetching
│   │   └── useScrollReveal.ts
│   ├── services/
│   │   └── api.ts           # API client
│   ├── styles/
│   │   ├── global.css
│   │   └── variables.css    # Theme colors
│   ├── types/
│   │   └── api.ts           # TypeScript interfaces
│   ├── App.tsx              # Main component
│   └── main.tsx             # Entry point
├── index.html
├── package.json
└── tsconfig.json
```

### Key Components

| Component | Purpose |
|-----------|---------|
| `App.tsx` | Root component, renders all sections |
| `Navbar` | Sticky navigation, theme toggle, mobile menu |
| `Hero` | Landing section with typing animation |
| `ContactForm` | Form with validation, email integration |
| `Badge`, `SectionHeader`, `LoadingSpinner` | Reusable UI components |

### State Management

- **Global:** Theme (ThemeContext)
- **Server:** Portfolio data (usePortfolio hook)
- **Local:** Form fields, UI state (useState)

### Theme System

```css
:root {
  /* Dark theme (default) */
  --color-primary: #0A0E27;
  --color-secondary: #6366F1;
  --color-accent: #10B981;
  --color-background: #0F1117;
}

[data-theme="light"] {
  /* Light theme */
  --color-primary: #FFFFFF;
  --color-secondary: #4F46E5;
  --color-accent: #059669;
}
```

- Persisted to localStorage
- Instant switching via CSS custom properties
- System preference detection

---

## 4. Backend Architecture

### Technology Stack

| Layer | Technology | Version |
|-------|------------|---------|
| Framework | FastAPI | 0.115.0+ |
| Language | Python | 3.10+ |
| Server | Uvicorn | 0.30.0+ |
| ORM | SQLAlchemy | 2.0.36+ |
| Validation | Pydantic | 2.9.0+ |
| Database | SQLite | 3.x |

### Folder Structure

```
backend/
├── app/
│   ├── routers/
│   │   ├── profile.py
│   │   ├── education.py
│   │   ├── experience.py
│   │   ├── skills.py
│   │   ├── projects.py
│   │   ├── certifications.py
│   │   ├── achievements.py
│   │   ├── contact.py       # Email integration
│   │   ├── resume.py        # File upload/download
│   │   └── summary.py       # Single endpoint for all data
│   ├── config.py            # Settings
│   ├── database.py          # DB connection
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── email_service.py     # SMTP email
│   └── main.py              # FastAPI app
├── uploads/resumes/
├── .env
├── portfolio.db
├── requirements.txt
└── run.py
```

### Database Schema (10 Tables)

| Table | Purpose | Key Fields |
|-------|---------|------------|
| `profiles` | User profile | full_name, title, bio, email, social_links |
| `education` | Academic history | degree, institution, dates, grade |
| `experiences` | Work experience | title, company, responsibilities[], technologies[] |
| `skills` | Technical skills | name, category, proficiency |
| `certifications` | Professional certs | name, issuer, credential_url |
| `projects` | Portfolio projects | name, description, technologies[], status |
| `achievements` | Awards | title, issuer, date, icon |
| `contact_messages` | Form submissions | name, email, message, is_read |
| `resumes` | Resume metadata | filename, file_path, is_active |

### API Endpoints

**Base URL:** `http://localhost:8000/api/v1`

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/summary/` | GET | **Primary** - All portfolio data in one request |
| `/profile/{id}` | GET, PATCH | Profile CRUD |
| `/education/` | GET, POST | Education list & create |
| `/experience/` | GET, POST | Experience list & create |
| `/skills/` | GET, POST | Skills list & create |
| `/projects/` | GET, POST | Projects list & create |
| `/certifications/` | GET, POST | Certifications |
| `/achievements/` | GET, POST | Achievements |
| `/contact/` | POST | Submit contact form |
| `/contact/messages` | GET | View all messages |
| `/resume/download` | GET | Download resume |
| `/resume/upload` | POST | Upload resume |

### Email Service

**Features:**
- SMTP email sending for contact forms
- HTML + plain text templates
- Gmail, Outlook, SendGrid support
- Graceful fallback (saves to DB even if email fails)

**Configuration (.env):**
```env
MAIL_ENABLED=True
MAIL_TO=your-email@example.com
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_TLS=True
```

---

## 5. Key Features

### 1. Dark/Light Theme Toggle

- Theme toggle button in navbar (sun/moon icon)
- Persisted to localStorage
- System preference detection
- Instant switching via CSS custom properties
- All UI elements automatically adapt

**Files:** `ThemeContext.tsx`, `variables.css`, `Navbar.tsx`

### 2. Contact Form with Email

- Client-side validation with real-time feedback
- Server-side Pydantic validation
- Saves to database
- Sends email via SMTP (optional)
- Success/error states

**Files:** `ContactForm.tsx`, `contact.py`, `email_service.py`

### 3. Single-Request Data Loading

- `/api/v1/summary` returns all portfolio data
- Reduces 10+ API calls to 1
- Includes computed stats
- Better performance

**Files:** `summary.py`, `usePortfolio.ts`

### 4. Responsive Design

- Mobile-first approach
- Hamburger menu on mobile
- Touch-friendly interactions
- Breakpoints: 768px, 1024px

### 5. Resume Download

- Upload via API
- Store metadata in database
- Direct download link
- Supports PDF, DOCX

**Files:** `resume.py`, Resume section in `App.tsx`

### 6. Smooth Navigation

- Hash-based scroll navigation
- Sticky navbar
- Active section highlighting
- Smooth scroll behavior

### 7. Typing Animation

- Character-by-character reveal
- Implemented with useEffect + setInterval
- In Hero component tagline

---

## 6. Data Flow

### Primary Flow

```
Browser loads → React App mounts
    ↓
usePortfolio() hook triggers
    ↓
GET /api/v1/summary
    ↓
FastAPI backend queries all tables
    ↓
Returns JSON with profile, education, experience, skills, projects, etc.
    ↓
React updates state and renders UI
```

### Contact Form Flow

```
User submits form → Validation
    ↓
POST /api/v1/contact/
    ↓
Backend validates → Save to DB → Send email
    ↓
Return success → Show success message
```

---

## 7. Security

### Frontend
- React XSS protection (auto-escaping)
- No secrets in code
- Input validation

### Backend
- SQL injection prevention (ORM)
- Pydantic validation on all endpoints
- CORS restricted to frontend origin
- Environment variables for secrets
- Email sanitization

---

## 8. Performance

### Frontend
- Vite optimized builds
- CSS Modules (no runtime cost)
- Single API request on load
- Tree-shaking

### Backend
- Single `/summary` endpoint (reduces requests)
- Database indexing
- SQLAlchemy connection pooling

---

## 9. Accessibility

- Semantic HTML (`<header>`, `<nav>`, `<main>`, `<section>`)
- ARIA labels where needed
- Keyboard navigation support
- Focus indicators
- Color contrast (WCAG AA)
- Alt text for images
- Form labels and error messages

---

## 10. Development Workflow

### Setup

```bash
# Backend
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python run.py  # → http://localhost:8000

# Frontend (new terminal)
cd frontend
npm install
npm run dev  # → http://localhost:5173
```

### Adding Content

Use Postman collection (`backend/postman_collection.json`) or API docs at http://localhost:8000/docs

---

## 11. Deployment

### Frontend Options
- **Vercel** (recommended)
- **Netlify**
- **GitHub Pages**
- **Azure Static Web Apps**

### Backend Options
- **Railway**
- **Render**
- **Heroku**
- **Azure App Service**
- **DigitalOcean**

### Production Env Variables
```env
DEBUG=False
ENVIRONMENT=production
CORS_ORIGINS=https://your-portfolio.vercel.app
MAIL_ENABLED=True
SMTP_HOST=smtp.sendgrid.net  # Use production email service
```

---

## 12. Technology Justifications

### Why React?
- Component reusability
- Type safety with TypeScript
- Large ecosystem and community
- Industry standard

### Why FastAPI?
- High performance (async)
- Auto-generated API docs
- Type safety with Pydantic
- Modern Python features

### Why SQLite?
- Zero configuration
- Single file database
- Sufficient for portfolio scale
- Easy to upgrade to PostgreSQL later

### Why TypeScript?
- Type safety catches errors early
- Better IDE support
- Self-documenting code
- Industry standard

### Why Vite?
- Fast HMR
- Optimized builds
- Modern tooling
- Better DX than Webpack

### Why CSS Modules?
- Scoped styles
- No naming conflicts
- Type-safe imports
- Zero runtime cost

---

## 13. Future Enhancements

### Phase 1 (Current) ✅
- [x] Full-stack application
- [x] Dark/light theme
- [x] Contact form with email
- [x] Resume download
- [x] Responsive design

### Phase 2 (Planned)
- [ ] Admin dashboard
- [ ] Blog section
- [ ] Project detail pages
- [ ] SEO optimization
- [ ] Analytics integration

### Phase 3 (Advanced)
- [ ] User authentication
- [ ] Image CDN (Cloudinary)
- [ ] Advanced animations
- [ ] PWA features
- [ ] i18n support

---

## 14. Documentation

Additional documentation available:

- **[QUICK_START.md](./QUICK_START.md)** - Get running in 5 minutes
- **[RUNNING_GUIDE.md](./RUNNING_GUIDE.md)** - Detailed setup guide
- **[FEATURES_GUIDE.md](./FEATURES_GUIDE.md)** - Complete features overview
- **[EMAIL_SETUP.md](./EMAIL_SETUP.md)** - Email configuration
- **[THEME_CUSTOMIZATION.md](./THEME_CUSTOMIZATION.md)** - Theme customization
- **[ADD_YOUR_PHOTO.md](./ADD_YOUR_PHOTO.md)** - Profile photo setup
- **[backend/README.md](./backend/README.md)** - Backend API documentation
- **[backend/TESTING_GUIDE.md](./backend/TESTING_GUIDE.md)** - API testing guide

---

## 15. API Documentation

Interactive API documentation available at:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **OpenAPI JSON:** http://localhost:8000/openapi.json

---

## 16. Summary

This portfolio demonstrates modern full-stack development practices:

✅ **Frontend:** React + TypeScript component architecture  
✅ **Backend:** RESTful API with FastAPI  
✅ **Database:** Relational data modeling with SQLAlchemy  
✅ **Features:** Theming, email integration, file upload  
✅ **Best Practices:** Type safety, validation, accessibility  
✅ **Performance:** Optimized builds, single-request loading  
✅ **Security:** Input validation, CORS, environment variables  

The architecture is production-ready, maintainable, and demonstrates proficiency with industry-standard tools and practices.
