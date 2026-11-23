# 🚀 Quick Start Guide

Get your portfolio running with theme switching and contact form in 5 minutes!

## Prerequisites

- ✅ Python 3.10+ installed
- ✅ Node.js 16+ installed
- ✅ Git installed

## Step 1: Start the Backend (2 minutes)

```bash
# Navigate to backend
cd backend

# Create virtual environment (first time only)
python -m venv venv

# Activate virtual environment
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# Install dependencies (first time only)
pip install -r requirements.txt

# Run the server
python run.py
```

✅ **Backend running** on http://localhost:8000  
📚 **API docs** at http://localhost:8000/docs

## Step 2: Start the Frontend (2 minutes)

Open a **new terminal**:

```bash
# Navigate to frontend
cd frontend

# Install dependencies (first time only)
npm install

# Start dev server
npm run dev
```

✅ **Frontend running** on http://localhost:5173

## Step 3: Test Features (1 minute)

### Test Theme Switching

1. Open http://localhost:5173
2. Look for the **sun/moon icon** in top-right corner
3. **Click it** - watch the colors change!
4. Refresh page - your theme choice persists ✨

### Test Contact Form

1. Scroll to **Contact section** (bottom of page)
2. Fill out the form:
   - Name: Your Name
   - Email: you@example.com
   - Message: Test message
3. Click **"Send Message"**
4. See the success message! ✅

## Step 4: Configure Email (Optional)

To receive emails when someone contacts you:

### Quick Gmail Setup

1. **Get an App Password**:
   - Visit https://myaccount.google.com/apppasswords
   - Select "Mail" and "Other"
   - Copy the generated password

2. **Edit `backend/.env`**:
```env
MAIL_ENABLED=True
MAIL_TO=your-email@gmail.com
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password-here
SMTP_TLS=True
```

3. **Restart backend**:
```bash
# Press Ctrl+C to stop
python run.py
```

4. **Test it**: Submit the contact form and check your email!

📖 **More providers**: See [EMAIL_SETUP.md](./EMAIL_SETUP.md)

## Verify Everything Works

### ✅ Checklist

- [ ] Backend running (http://localhost:8000)
- [ ] Frontend running (http://localhost:5173)
- [ ] Can see portfolio content
- [ ] Theme toggle button visible (sun/moon icon)
- [ ] Clicking theme button changes colors
- [ ] Contact form visible at bottom
- [ ] Can submit contact form
- [ ] See success message after submission
- [ ] Email configured (optional)

## Common Issues

### Port Already in Use

**Backend (port 8000)**:
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:8000 | xargs kill -9
```

**Frontend (port 5173)**:
```bash
# Windows
netstat -ano | findstr :5173
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:5173 | xargs kill -9
```

### Module Not Found

```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

### Database Doesn't Exist

```bash
cd backend
python create_sample_resume.py
```

## Next Steps

### Customize Your Portfolio

1. **Update Colors**: Edit `frontend/src/styles/variables.css`
2. **Add Your Content**: Use the API to update profile, projects, etc.
3. **Customize Form**: Edit `frontend/src/components/Contact/ContactForm.tsx`

### Learn More

- 📚 [FEATURES_GUIDE.md](./FEATURES_GUIDE.md) - Complete features overview
- 🎨 [THEME_CUSTOMIZATION.md](./THEME_CUSTOMIZATION.md) - Customize themes
- 📧 [EMAIL_SETUP.md](./EMAIL_SETUP.md) - Email configuration
- 🏗️ [architecture.md](./architecture.md) - System architecture

## Quick Reference

```bash
# Backend
cd backend
python run.py
# → http://localhost:8000

# Frontend
cd frontend  
npm run dev
# → http://localhost:5173

# View Messages
curl http://localhost:8000/api/v1/contact/messages

# API Docs
http://localhost:8000/docs
```

## What You Get

✨ **Theme Switching**:
- Dark mode (default)
- Light mode
- Persistent preference
- Smooth transitions

📧 **Contact Form**:
- Real-time validation
- Database storage
- Email notifications (optional)
- Success/error feedback

🎨 **Modern UI**:
- Responsive design
- Smooth animations
- Professional styling
- Mobile-friendly

---

## 🎉 That's It!

Your portfolio is now running with:
- ✅ Working theme switcher
- ✅ Functional contact form
- ✅ Beautiful, responsive design

**Enjoy!** 🚀

Need help? Check [FEATURES_GUIDE.md](./FEATURES_GUIDE.md) or [SETUP_COMPLETE.md](./SETUP_COMPLETE.md)
