# Portfolio Frontend

Modern React + TypeScript portfolio website integrated with FastAPI backend.

## Quick Start

```powershell
# Install dependencies
npm install

# Start development server (requires backend running on :8000)
npm run dev

# Build for production
npm run build
```

## Development

Frontend runs on: `http://localhost:5173`
Backend API proxy: `/api` → `http://localhost:8000/api`

## Features

- ✅ Fully integrated with Backend API (`/api/v1/summary`)
- ✅ TypeScript for type safety
- ✅ Responsive design (mobile-first)
- ✅ Smooth scroll animations
- ✅ Typing effect in hero
- ✅ Contact form integration
- ✅ Resume download
- ✅ Dark professional design following architecture.md

## Structure

```
frontend/
├── src/
│   ├── components/      # All React components
│   ├── hooks/           # Custom React hooks
│   ├── services/        # API layer
│   ├── styles/          # Global CSS
│   └── types/           # TypeScript types
├── public/              # Static assets
└── vite.config.ts       # Vite configuration with API proxy
```

## Architecture Compliance

All design tokens, colors, fonts, and components follow `architecture.md` specifications:
- Colors: #0F172A (primary), #1D4ED8 (secondary), #14B8A6 (accent)
- Fonts: Poppins (headings), Inter (body), Space Grotesk (display)
- Sections: Hero, About, Education, Experience, Skills, Projects, Achievements, Resume, Contact

## Commands

- `npm run dev` — Start dev server with HMR
- `npm run build` — Build for production
- `npm run preview` — Preview production build
- `npm run lint` — Run ESLint

## Backend Integration

The frontend uses `/api/v1/summary` endpoint to fetch all portfolio data in a single request on page load. See `src/services/api.ts` for API client implementation.
