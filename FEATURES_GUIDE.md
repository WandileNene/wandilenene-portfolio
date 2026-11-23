# Portfolio Features Guide

Complete guide to your portfolio's features, including theme switching and contact form.

## 🎨 Theme Switching (Dark/Light Mode)

### Overview
Your portfolio includes a fully functional dark/light theme switcher that allows visitors to choose their preferred viewing mode.

### How It Works

**For Visitors:**
1. Look for the sun/moon icon in the top navigation bar (top right)
2. Click the icon to toggle between dark and light modes
3. Your preference is automatically saved and will persist across visits

**Icon Indicators:**
- ☀️ **Sun icon** = Currently in dark mode (click to switch to light)
- 🌙 **Moon icon** = Currently in light mode (click to switch to dark)

### Technical Details

The theme system includes:
- ✅ Dark and light color schemes
- ✅ Smooth transitions between themes
- ✅ Persistent theme preference (saved to browser)
- ✅ System theme detection (respects OS preference)
- ✅ All UI elements automatically adapt

**Files Involved:**
- `frontend/src/context/ThemeContext.tsx` - Theme state management
- `frontend/src/styles/variables.css` - Color definitions for both themes
- `frontend/src/components/Navbar/Navbar.tsx` - Theme toggle button

### Customizing Colors

See [`THEME_CUSTOMIZATION.md`](./THEME_CUSTOMIZATION.md) for detailed instructions on customizing the color schemes.

---

## 📧 Contact Form

### Overview
The contact form allows visitors to send you messages directly from your portfolio. Messages are saved to the database and can optionally send email notifications.

### How It Works

**For Visitors:**
1. Navigate to the "Contact" section (bottom of the page or click Contact in nav)
2. Fill in the form:
   - **Name** (required)
   - **Email** (required)
   - **Subject** (optional)
   - **Message** (required, min 10 characters)
3. Click "Send Message"
4. See success confirmation

**For You (Portfolio Owner):**

#### Option 1: Database Storage (Default - No Setup Required)
All messages are automatically saved to your SQLite database. You can view them:

```bash
# Using curl
curl http://localhost:8000/api/v1/contact/messages

# Or import the Postman collection
# backend/postman_collection.json
```

#### Option 2: Email Notifications (Requires Setup)
Configure SMTP settings to receive email notifications when someone contacts you.

**Quick Setup:**
1. Edit `backend/.env` and add your email settings:
```env
MAIL_ENABLED=True
MAIL_TO=your-email@example.com
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

2. Restart the backend:
```bash
cd backend
python run.py
```

**See [`EMAIL_SETUP.md`](./EMAIL_SETUP.md) for detailed setup instructions**, including:
- Gmail configuration (recommended for personal use)
- Outlook/Hotmail setup
- SendGrid/Mailgun (recommended for production)
- Troubleshooting guide

### What Happens When Someone Submits

1. ✅ Message is validated (required fields, email format, etc.)
2. 💾 Message is saved to the database
3. ✉️ Email notification is sent (if configured)
4. 🎉 Success message is shown to visitor

Even if email is not configured, messages are still saved to the database, so you won't lose any inquiries.

### Form Features

- ✅ **Real-time validation** - Instant feedback as you type
- ✅ **Accessibility compliant** - Screen reader friendly
- ✅ **Spam protection** - Server-side validation
- ✅ **Character counter** - Shows message length
- ✅ **Error handling** - Clear error messages
- ✅ **Success confirmation** - Visual feedback

### Security Features

- Input sanitization
- Email format validation
- CORS protection
- Rate limiting ready (can be added)
- No client-side email exposure

---

## 🔗 Other Portfolio Features

### 📱 Responsive Design
- Mobile-first approach
- Hamburger menu on mobile devices
- Touch-friendly interactions
- Optimized for all screen sizes

### 🎯 Smooth Navigation
- Smooth scrolling between sections
- Active section highlighting in navbar
- Sticky navbar with blur effect
- Auto-scroll on link click

### 📄 Resume Download
- One-click resume download
- PDF format
- Direct download from server
- Upload your resume via API

### 🎨 Modern UI Elements

**Sections:**
- Hero/Introduction
- About Me
- Education
- Experience
- Skills (categorized)
- Projects (with featured badges)
- Achievements
- Resume Download
- Contact Form

**Components:**
- Loading spinner
- Section headers
- Badges (for dates, status)
- Tags (for skills, technologies)
- Cards (with hover effects)
- Smooth animations

### ⚡ Performance

- Fast API with single-request summary endpoint
- Optimized bundle size
- CSS custom properties for instant theme switching
- Lazy loading ready
- Efficient state management

---

## 🚀 Getting Started

### Running the Portfolio

**Backend (FastAPI):**
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python run.py
```

Backend runs on: `http://localhost:8000`
API docs: `http://localhost:8000/docs`

**Frontend (React + Vite):**
```bash
cd frontend
npm install
npm run dev
```

Frontend runs on: `http://localhost:5173`

### First-Time Setup

1. **Database**: Automatically created on first run
2. **Sample Data**: Run `backend/create_sample_resume.py` to seed data
3. **Email** (optional): Configure in `backend/.env` (see EMAIL_SETUP.md)
4. **Customization**: Edit colors in `frontend/src/styles/variables.css`

---

## 📚 Documentation

- **[RUNNING_GUIDE.md](./RUNNING_GUIDE.md)** - How to run the project
- **[architecture.md](./architecture.md)** - System architecture
- **[EMAIL_SETUP.md](./EMAIL_SETUP.md)** - Email configuration
- **[THEME_CUSTOMIZATION.md](./THEME_CUSTOMIZATION.md)** - Theme customization
- **[backend/README.md](./backend/README.md)** - Backend API docs
- **[backend/TESTING_GUIDE.md](./backend/TESTING_GUIDE.md)** - API testing guide

---

## 🎯 Quick Reference

### Theme Toggle
- **Location**: Top right of navbar (sun/moon icon)
- **Shortcut**: Click the icon
- **Persistence**: Automatic (localStorage)

### Contact Form
- **Location**: Bottom of page (Contact section)
- **Email Setup**: See EMAIL_SETUP.md
- **View Messages**: API endpoint `/api/v1/contact/messages`

### API Endpoints
- `GET /api/v1/summary/` - Full portfolio data
- `POST /api/v1/contact/` - Submit contact form
- `GET /api/v1/contact/messages` - View all messages
- `GET /api/v1/resume/download` - Download resume

### Customization
- **Colors**: `frontend/src/styles/variables.css`
- **Content**: Update via API or edit seed data
- **Email**: `backend/.env`
- **Styling**: Component-specific `.module.css` files

---

## 🐛 Troubleshooting

### Theme Not Switching
- Check browser console for errors
- Verify ThemeProvider is wrapping App component
- Clear browser cache/localStorage

### Contact Form Not Working
- Check backend is running (`http://localhost:8000`)
- Verify CORS settings in `backend/app/config.py`
- Check network tab in browser DevTools

### Email Not Sending
- Verify `MAIL_ENABLED=True` in `.env`
- Check SMTP credentials
- See EMAIL_SETUP.md for provider-specific help
- Messages still save to database even if email fails

### General Issues
- Restart both backend and frontend
- Check for error messages in terminal
- Verify all dependencies are installed
- Check that ports 8000 and 5173 are not in use

---

## 💡 Tips & Tricks

### Development
- Use the API docs at `/docs` for testing endpoints
- Import `backend/postman_collection.json` for API testing
- Check browser console for React errors
- Use React DevTools for component debugging

### Customization
- Start with color variables before editing components
- Test both themes when making changes
- Use the existing component patterns
- Follow the established naming conventions

### Production
- Set `DEBUG=False` in backend `.env`
- Use a production-ready SMTP service (SendGrid, etc.)
- Add rate limiting to contact form
- Enable HTTPS
- Add CAPTCHA to contact form
- Configure proper CORS origins

---

## 📞 Support

If you encounter issues:

1. Check the relevant documentation file
2. Search for error messages in the code
3. Check backend logs
4. Test with default/sample configuration
5. Verify environment variables are set correctly

---

## 🎉 Enjoy Your Portfolio!

Your portfolio now has:
- ✅ Professional dark/light theme switcher
- ✅ Fully functional contact form with email support
- ✅ Modern, responsive design
- ✅ Easy customization
- ✅ Comprehensive documentation

Happy showcasing! 🚀
