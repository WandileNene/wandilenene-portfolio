# Portfolio API — Postman Testing Guide

Complete step-by-step guide for testing all backend API endpoints using Postman.

---

## ✅ Prerequisites

1. **Backend server running** on `http://localhost:8000`
2. **Postman** installed ([Download](https://www.postman.com/downloads/))
3. **Postman collection** imported: `postman_collection.json`

---

## 🚀 Quick Start

### Step 1: Start the Server

```powershell
cd C:\Users\WandileNene\portfolio_copilot\backend
.\venv\Scripts\python.exe run.py
```

**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

### Step 2: Import Collection into Postman

1. Open **Postman**
2. Click **Import** (top-left corner)
3. Drag `postman_collection.json` into the import dialog
4. Click **Import**

The collection **"Portfolio API - Wandile Nene"** will appear in your workspace.

### Step 3: Verify Collection Variables

1. Click the collection name
2. Go to **Variables** tab
3. Confirm:
   - `baseUrl` = `http://localhost:8000`
   - `apiVersion` = `api/v1`

---

## 📋 Testing Plan — Phase by Phase

Work through each folder in order. Each phase tests a different part of the API.

---

### **Phase 1: Health Check** 🏥

Test that the API is up and responding.

| Request | Expected | What to Check |
|---|---|---|
| `GET /` | `200 OK` | Returns `name`, `version`, `status: running`, `docs`, `api_prefix` |
| `GET /health` | `200 OK` | Returns `status: healthy`, `version`, `environment` |

**Validation:**
- Both return JSON
- Status code is `200`
- Response time < 100ms

---

### **Phase 2: Summary Endpoint** 📋

The power endpoint — returns all portfolio data in one JSON response.

| Request | Expected | What to Check |
|---|---|---|
| `GET /api/v1/summary/` | `200 OK` | Full portfolio JSON with profile, education, experience, skills (grouped), certifications, projects, achievements, and stats |

**Validation:**
- Response contains all 8 keys: `profile`, `education`, `experience`, `skills`, `certifications`, `projects`, `achievements`, `stats`
- `skills` is a dictionary grouped by category (5 categories)
- `stats.total_projects` = 4
- `stats.featured_projects` = 2
- Response size > 10KB

---

### **Phase 3: Profile Management** 👤

Manage the portfolio owner's profile.

| Request | Method | Expected | Notes |
|---|---|---|---|
| GET Profile | `GET` | `200 OK` | Returns Wandile Nene's profile |
| PATCH Profile | `PATCH` | `200 OK` | Update title or bio |
| POST Profile (2nd time) | `POST` | `409 Conflict` | Only one profile allowed |

**Validation:**
- GET returns `full_name: "Wandile Nene"`
- PATCH with `{"title": "Senior AI Engineer"}` updates the title
- POST fails with `409` if profile already exists

**Test Flow:**
1. `GET /api/v1/profile/` — confirm profile exists
2. `PATCH /api/v1/profile/` with `{"tagline": "Updated tagline"}` — confirm update
3. `GET /api/v1/profile/` again — confirm tagline changed

---

### **Phase 4: Education** 🎓

| Request | Expected | Notes |
|---|---|---|
| GET All | `200 OK` | 1 education record (BSc Computer Science) |
| GET by ID | `200 OK` | Single record |
| POST Create | `201 Created` | New education entry |
| PATCH Update | `200 OK` | Update grade or description |
| DELETE | `200 OK` | Delete education entry |

**Validation:**
- Default data has 1 education entry
- POST with new degree adds successfully
- PATCH updates fields
- GET by invalid ID returns `404`

---

### **Phase 5: Experience** 💼

| Request | Expected | Notes |
|---|---|---|
| GET All | `200 OK` | 3 experience entries |
| GET ?is_current=true | `200 OK` | Only AI Engineer Intern |
| GET ?employment_type=Internship | `200 OK` | Filtered by type |
| POST Create | `201 Created` | New experience entry |
| PATCH Update | `200 OK` | Update description |
| DELETE | `200 OK` | Delete experience entry |

**Validation:**
- Default data has 3 experience entries
- Filter `is_current=true` returns 1 result
- `responsibilities` and `technologies` are JSON arrays

---

### **Phase 6: Skills** 🛠️

| Request | Expected | Notes |
|---|---|---|
| GET All | `200 OK` | 23 skills total |
| GET Grouped | `200 OK` | Dictionary with 5 categories |
| GET Categories | `200 OK` | List of 5 category names |
| GET ?category=Languages | `200 OK` | 6 language skills |
| POST Create | `201 Created` | New skill entry |
| PATCH Update | `200 OK` | Update proficiency |
| DELETE | `200 OK` | Delete skill |

**Validation:**
- `/grouped` returns `{"categories": {...}}`
- `/categories` returns `["AI / ML", "Databases", ...]`
- Proficiency is between 0–100

---

### **Phase 7: Certifications** 🏅

| Request | Expected | Notes |
|---|---|---|
| GET All | `200 OK` | 3 certifications |
| POST Create | `201 Created` | New certification |
| PATCH Update | `200 OK` | Update expiry date |
| DELETE | `200 OK` | Delete certification |

**Validation:**
- `credential_url` is optional
- `expiry_date` is optional

---

### **Phase 8: Projects** 🚀

| Request | Expected | Notes |
|---|---|---|
| GET All | `200 OK` | 4 projects |
| GET Featured | `200 OK` | 2 featured projects |
| GET by Slug | `200 OK` | Get by slug (e.g., `portfolio-rest-api`) |
| GET ?status=in-progress | `200 OK` | 1 in-progress project |
| POST Create | `201 Created` | New project |
| PATCH Update | `200 OK` | Update status or featured flag |
| DELETE | `200 OK` | Delete project |

**Validation:**
- `slug` must be unique (409 on duplicate)
- `/featured` returns only `is_featured: true`
- `technologies` and `features` are arrays

---

### **Phase 9: Achievements** 🏆

| Request | Expected | Notes |
|---|---|---|
| GET All | `200 OK` | 4 achievements |
| POST Create | `201 Created` | New achievement |
| PATCH Update | `200 OK` | Update description |
| DELETE | `200 OK` | Delete achievement |

**Validation:**
- Each achievement has `title`, `issuer`, `date`
- `icon` is optional

---

### **Phase 10: Contact Messages** 📬

| Request | Expected | Notes |
|---|---|---|
| POST Send Message | `201 Created` | New message saved |
| GET All Messages | `200 OK` | All messages (admin) |
| GET ?is_read=false | `200 OK` | Only unread messages |
| PATCH Mark as Read | `200 OK` | Sets `is_read: true` |
| DELETE Message | `200 OK` | Delete message |

**Validation:**
- POST returns `is_read: false` by default
- Email must be valid format
- `name` and `message` are required

**End-to-End Flow:**
1. POST new message
2. GET all messages — confirm it's there with `is_read: false`
3. PATCH mark as read
4. GET `?is_read=false` — confirm it's no longer in unread list

---

### **Phase 11: Resume Management** 📄

This is the new feature you requested — view and download resume files.

| Request | Method | Expected | Notes |
|---|---|---|---|
| GET Metadata | `GET /api/v1/resume/` | `200 OK` | Returns active resume metadata |
| GET All Versions | `GET /api/v1/resume/all` | `200 OK` | All resume versions (active + inactive) |
| **Download Active** | `GET /api/v1/resume/download` | `200 OK` | **Downloads the currently active resume file** |
| Download by ID | `GET /api/v1/resume/download/1` | `200 OK` | Downloads specific version |
| Upload Resume | `POST /api/v1/resume/upload` | `201 Created` | Upload a PDF/DOCX resume file |
| Activate Resume | `PATCH /api/v1/resume/1/activate` | `200 OK` | Set version 1 as active |
| Delete Resume | `DELETE /api/v1/resume/1` | `200 OK` | Delete resume file and metadata |

#### **How to Test Resume Upload in Postman**

1. Open `POST Upload Resume` request
2. Go to **Body** tab
3. Ensure **form-data** is selected
4. Set up the fields:
   - `file` (type: **File**) — click **Select Files** and choose a PDF or DOCX resume
   - `version` (type: **Text**) — e.g., `v2024.08`
   - `description` (type: **Text**) — e.g., `Latest resume with AI experience`
5. Click **Send**

**Expected Response:**
```json
{
  "id": 2,
  "filename": "resume_20240806_101530.pdf",
  "original_filename": "Wandile_Nene_Resume.pdf",
  "file_size": 125340,
  "content_type": "application/pdf",
  "version": "v2024.08",
  "description": "Latest resume with AI experience",
  "is_active": true,
  "created_at": "2024-08-06T10:15:30.123456",
  "updated_at": "2024-08-06T10:15:30.123456"
}
```

#### **How to Test Resume Download**

**Option 1: Using Postman**
1. Open `GET Download Active Resume`
2. Click **Send**
3. Click **Save Response** → **Save to a file**
4. Choose a location and filename (e.g., `downloaded_resume.pdf`)
5. Open the file to verify it's correct

**Option 2: Using Your Browser**
1. Go to: `http://localhost:8000/api/v1/resume/download`
2. The resume file downloads automatically
3. Open the file to verify

**Validation:**
- Sample resume is pre-loaded on first run (plain text version)
- Upload accepts only PDF and DOCX (max 10MB)
- Only one resume can be active at a time
- Download returns the correct `Content-Type` header
- Downloaded file matches the uploaded file

**End-to-End Resume Flow:**
1. `GET /api/v1/resume/` — Check current active resume
2. `GET /api/v1/resume/download` — Download the active resume
3. `POST /api/v1/resume/upload` — Upload a new version
4. `GET /api/v1/resume/all` — See both versions (old one is now inactive)
5. `PATCH /api/v1/resume/1/activate` — Reactivate the old version
6. `GET /api/v1/resume/download` — Download now returns the old version

---

## 🎯 Critical Scenarios to Test

### Scenario 1: First-Time User Experience
1. `GET /` — API info
2. `GET /api/v1/summary/` — Full portfolio in one call
3. `GET /api/v1/resume/download` — Get the resume

### Scenario 2: Recruiter Interaction
1. `GET /api/v1/profile/` — View candidate profile
2. `GET /api/v1/projects/featured` — View featured projects
3. `GET /api/v1/resume/download` — Download resume
4. `POST /api/v1/contact/` — Send message to candidate

### Scenario 3: Content Management
1. `POST /api/v1/projects/` — Add new project
2. `PATCH /api/v1/projects/1` — Mark as featured
3. `POST /api/v1/certifications/` — Add new certification
4. `POST /api/v1/resume/upload` — Upload updated resume

### Scenario 4: Error Handling
1. `GET /api/v1/projects/999` — 404 Not Found
2. `POST /api/v1/projects/` with duplicate slug — 409 Conflict
3. `PATCH /api/v1/profile/` with invalid email — 422 Validation Error

---

## 🐛 Common Issues & Solutions

### Issue: "Connection refused" or "Cannot connect"
**Solution:** Server is not running. Start it with:
```powershell
.\venv\Scripts\python.exe run.py
```

### Issue: "404 Not Found" on all `/api/v1/*` requests
**Solution:** Check collection variables. Ensure `apiVersion` = `api/v1` (no leading slash).

### Issue: Resume upload fails with "Invalid file type"
**Solution:** Only PDF and DOCX are allowed. Check file extension.

### Issue: Resume download returns 404
**Solution:** No active resume. Upload one first using `POST /api/v1/resume/upload`.

### Issue: "422 Validation Error"
**Solution:** Required field is missing or format is wrong. Check the error details in the response.

---

## 📊 Success Metrics

After running all tests, you should have:
- ✅ All health checks passing
- ✅ Summary endpoint returning full portfolio
- ✅ Profile created and updated
- ✅ Education, Experience, Skills, Certifications, Projects, Achievements all CRUD operations working
- ✅ Contact message flow working end-to-end
- ✅ **Resume upload, download, and version management working**
- ✅ All error scenarios handled gracefully
- ✅ No 500 Internal Server Errors

---

## 🌐 Alternative: Swagger UI

Instead of Postman, you can also use the built-in **Swagger UI** for interactive testing:

1. Go to: `http://localhost:8000/docs`
2. Expand any endpoint
3. Click **Try it out**
4. Fill in the parameters/body
5. Click **Execute**

The Swagger UI auto-generates forms for every endpoint and shows example responses.

**For Resume Upload in Swagger:**
1. Go to `POST /api/v1/resume/upload`
2. Click **Try it out**
3. Click **Choose File** under the `file` field
4. Fill optional `version` and `description` fields
5. Click **Execute**

---

## 🎉 Next Steps

Once you've verified all endpoints work correctly:
1. **Frontend Integration** — Connect your React/Next.js frontend to these APIs
2. **Authentication** — Add JWT tokens for admin endpoints (optional)
3. **Deployment** — Deploy to cloud (Railway, Render, AWS, Azure)
4. **CI/CD** — Set up automated testing pipeline

---

**Happy Testing!** 🚀

For questions or issues, check the server logs or the FastAPI docs at `http://localhost:8000/docs`.
