# Portfolio — How to Run Locally

Complete guide to running both backend and frontend together.

---

## ✅ Prerequisites

- Python 3.11+ installed
- Node.js 18+ and npm installed
- Both backend and frontend folders exist in `portfolio_copilot/`

---

## 🚀 Quick Start (Backend + Frontend)

### Option 1: Run Everything (Two Terminals)

**Terminal 1 — Backend:**
```powershell
cd C:\Users\WandileNene\portfolio_copilot\backend
.\venv\Scripts\python.exe run.py
```

**Terminal 2 — Frontend:**
```powershell
cd C:\Users\WandileNene\portfolio_copilot\frontend
npm run dev
```

**Then open:** `http://localhost:5173`

---

## 📋 Step-by-Step First-Time Setup

### 1. Backend Setup (One-Time)

```powershell
# Navigate to backend
cd C:\Users\WandileNene\portfolio_copilot\backend

# Create virtual environment (if not exists)
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Seed database with portfolio data
python -m app.seed_data

# Start backend server
python run.py
```

**Backend will start on:** `http://localhost:8000`

**Verify backend:**
- Open: `http://localhost:8000/docs` (Swagger UI)
- Should see interactive API documentation

### 2. Frontend Setup (One-Time)

Open a **NEW terminal window** (keep backend running in the first one):

```powershell
# Navigate to frontend
cd C:\Users\WandileNene\portfolio_copilot\frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

**Frontend will start on:** `http://localhost:5173`

**Verify frontend:**
- Open: `http://localhost:5173`
- Should see the portfolio website with:
  - Navbar at the top
  - Hero section with Wandile Nene's name
  - About, Education, Experience, Skills, Projects sections
  - Download Resume button
  - Contact section

---

## 🔍 Verification Checklist

### Backend (Port 8000)

✅ Health Check:
```powershell
curl http://localhost:8000/health
```
Expected: `{"status":"healthy","version":"1.0.0"}`

✅ API Summary:
```powershell
curl http://localhost:8000/api/v1/summary/
```
Expected: Large JSON with profile, education, experience, skills, projects, etc.

✅ Swagger UI:
- Open `http://localhost:8000/docs`
- Should see all endpoints listed

### Frontend (Port 5173)

✅ Homepage loads:
- Open `http://localhost:5173`
- Navbar visible at top
- Hero section shows "Hi, I'm Wandile Nene"
- Typing animation in tagline

✅ Navigation works:
- Click "About" in navbar → scrolls smoothly
- Click "Projects" → scrolls to projects section
- All sections load with real data from backend

✅ Data integration:
- Profile name shows: "Wandile Nene"
- Experience shows 3 entries (AI Engineer Intern, Tutor, Bootcamp)
- Skills show 23 skills in 5 categories
- Projects show 4 projects

✅ Resume download:
- Click "Resume" in navbar or scroll to Resume section
- Click "Download Resume" button
- A text file should download

---

## 🐛 Troubleshooting

### Issue: "Connection refused" on frontend

**Problem:** Backend is not running.

**Solution:**
```powershell
cd C:\Users\WandileNene\portfolio_copilot\backend
.\venv\Scripts\python.exe run.py
```

### Issue: Frontend shows blank page or error

**Problem:** Frontend dependencies not installed or backend not responding.

**Solution:**
```powershell
# Reinstall frontend dependencies
cd C:\Users\WandileNene\portfolio_copilot\frontend
npm install

# Verify backend is running
curl http://localhost:8000/health

# Restart frontend
npm run dev
```

### Issue: "Module not found" errors

**Problem:** TypeScript/React dependencies missing.

**Solution:**
```powershell
cd C:\Users\WandileNene\portfolio_copilot\frontend
rm -r node_modules
rm package-lock.json
npm install
```

### Issue: Backend port 8000 already in use

**Problem:** Another process is using port 8000.

**Solution:**
```powershell
# Find and kill the process
Get-Process -Name python | Where-Object {$_.Path -like "*portfolio*"} | Stop-Process -Force

# Or change port in backend/.env:
# PORT=8001
```

### Issue: CORS errors in browser console

**Problem:** Backend CORS not configured for frontend.

**Solution:** Already fixed! The backend `.env` includes `http://localhost:5173` in `CORS_ORIGINS`.

---

## 📊 What You Should See

### Backend Terminal
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using WatchFiles
INFO:     Started server process [67890]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Frontend Terminal
```
  VITE v5.4.2  ready in 543 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

### Browser (http://localhost:5173)
- ✅ Portfolio website loads
- ✅ Smooth scrolling navigation
- ✅ Typing animation in hero
- ✅ All sections populated with real data
- ✅ Resume download button works
- ✅ No console errors

---

## 🛑 Stopping the Servers

**Backend:**
- Go to the terminal running `python run.py`
- Press `Ctrl+C`

**Frontend:**
- Go to the terminal running `npm run dev`
- Press `Ctrl+C`

---

## 🔄 Daily Development Workflow

Once everything is set up, you only need:

1. **Start Backend:**
   ```powershell
   cd C:\Users\WandileNene\portfolio_copilot\backend
   .\venv\Scripts\python.exe run.py
   ```

2. **Start Frontend (new terminal):**
   ```powershell
   cd C:\Users\WandileNene\portfolio_copilot\frontend
   npm run dev
   ```

3. **Open browser:** `http://localhost:5173`

---

## 🎯 Next Steps

Once you verify everything works:

1. **Customize content:**
   - Update `backend/.env` with real email, phone
   - Replace placeholder profile image
   - Update projects, skills, certifications via Postman or directly in seed_data.py

2. **Upload real resume:**
   - Use Postman: `POST /api/v1/resume/upload`
   - Or use Swagger UI: `http://localhost:8000/docs`

3. **Deploy:**
   - Backend: Railway, Render, or AWS
   - Frontend: Vercel, Netlify, or GitHub Pages (after build)

---

## 📞 Support

If something doesn't work:

1. Check both terminals for error messages
2. Verify both ports are accessible:
   - `curl http://localhost:8000/health`
   - Open `http://localhost:5173` in browser
3. Check browser console (F12) for JavaScript errors
4. Restart both servers

---

**Enjoy your portfolio! 🚀**
