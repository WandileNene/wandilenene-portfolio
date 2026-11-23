# 📸 How to Add Your Profile Picture

There are **three easy ways** to add your picture to the portfolio. Choose the method that works best for you!

---

## Method 1: Use a Direct Image URL (Easiest) ⭐

If your picture is already hosted online (LinkedIn, GitHub, Imgur, etc.), you can use the URL directly.

### Step 1: Get Your Image URL

**From LinkedIn:**
1. Open your LinkedIn profile
2. Right-click your profile picture → "Copy image address"
3. You'll get a URL like: `https://media.licdn.com/dms/image/...`

**From GitHub:**
1. Go to your GitHub profile
2. Right-click your avatar → "Copy image address"
3. You'll get a URL like: `https://avatars.githubusercontent.com/u/...`

**From Imgur (recommended):**
1. Go to https://imgur.com
2. Upload your picture
3. Get the direct link (right-click → "Copy image address")

### Step 2: Update Your Profile via API

**Option A: Using curl (Command Line)**

```bash
curl -X PATCH http://localhost:8000/api/v1/profile/1 \
  -H "Content-Type: application/json" \
  -d "{\"profile_image\": \"YOUR_IMAGE_URL_HERE\"}"
```

**Option B: Using Postman**

1. Import `backend/postman_collection.json`
2. Find "Update Profile" request
3. Change `profile_image` field to your URL
4. Click Send

**Example:**
```json
{
  "profile_image": "https://avatars.githubusercontent.com/u/12345678"
}
```

### Step 3: Refresh Your Portfolio

Refresh http://localhost:5173 - your picture should appear!

---

## Method 2: Host Your Image Locally (Recommended for Production) 🏠

Store your image in your project and reference it.

### Step 1: Add Your Image File

Copy your image to the frontend public folder:

```
frontend/public/
  └── images/
      └── profile.jpg    ← Your picture here
```

**Create the images folder:**
```bash
cd frontend/public
mkdir images
# Then copy your image file into this folder
```

### Step 2: Update Your Profile

Update the database to use the local path:

```bash
curl -X PATCH http://localhost:8000/api/v1/profile/1 \
  -H "Content-Type: application/json" \
  -d "{\"profile_image\": \"/images/profile.jpg\"}"
```

### Step 3: Verify

1. Check the file exists: `frontend/public/images/profile.jpg`
2. Refresh your portfolio
3. Your picture should display!

**Supported formats:** `.jpg`, `.jpeg`, `.png`, `.webp`, `.gif`

---

## Method 3: Use Backend Upload (Advanced) 📤

Upload your image through the backend API for better control.

### Step 1: Create Upload Directory

```bash
cd backend
mkdir -p uploads/profile
```

### Step 2: Copy Your Image

```bash
# Copy your image file to the uploads folder
copy C:\path\to\your\photo.jpg backend\uploads\profile\profile.jpg
```

### Step 3: Update Your Profile

```bash
curl -X PATCH http://localhost:8000/api/v1/profile/1 \
  -H "Content-Type: application/json" \
  -d "{\"profile_image\": \"/uploads/profile/profile.jpg\"}"
```

### Step 4: Serve Static Files (if needed)

The backend should serve static files from the uploads directory. Check `backend/app/main.py` to ensure this is configured.

---

## Quick Test Script

Here's a script to quickly update your profile picture:

### Windows PowerShell:
```powershell
# Replace with your image URL
$imageUrl = "https://avatars.githubusercontent.com/u/12345678"

# Update profile
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/profile/1" `
  -Method PATCH `
  -ContentType "application/json" `
  -Body (@{profile_image = $imageUrl} | ConvertTo-Json)

Write-Host "✅ Profile picture updated! Refresh your browser."
```

### Linux/Mac:
```bash
#!/bin/bash
# Replace with your image URL
IMAGE_URL="https://avatars.githubusercontent.com/u/12345678"

# Update profile
curl -X PATCH http://localhost:8000/api/v1/profile/1 \
  -H "Content-Type: application/json" \
  -d "{\"profile_image\": \"$IMAGE_URL\"}"

echo "✅ Profile picture updated! Refresh your browser."
```

---

## Viewing Your Current Profile Picture

Check what image URL is currently set:

```bash
curl http://localhost:8000/api/v1/profile/1 | grep profile_image
```

Or visit the API docs: http://localhost:8000/docs
- Go to `GET /api/v1/profile/{profile_id}`
- Try it out with ID `1`
- Check the `profile_image` field

---

## Troubleshooting

### Picture Not Displaying

**1. Check the URL is accessible:**
```bash
# Test if the URL works
curl -I YOUR_IMAGE_URL
```

**2. Check for CORS issues:**
- Some sites block hotlinking (using their images on other sites)
- If using LinkedIn/GitHub, this shouldn't be an issue
- For other sites, download and host locally instead

**3. Check the file path (local images):**
```bash
# Verify the file exists
dir frontend\public\images\profile.jpg   # Windows
ls frontend/public/images/profile.jpg     # Mac/Linux
```

**4. Clear browser cache:**
- Press `Ctrl + Shift + R` (Windows/Linux)
- Press `Cmd + Shift + R` (Mac)

**5. Check the database value:**
```bash
curl http://localhost:8000/api/v1/profile/1
```

### Image Too Large/Small

The image will be automatically sized to fit the design. For best results:

- **Recommended size**: 400x400 pixels or larger
- **Aspect ratio**: Square (1:1) works best
- **File size**: Under 500KB for fast loading
- **Format**: JPG or PNG (WebP for best performance)

### Profile Picture Shows Placeholder

If you see a broken image or placeholder:

1. Check that `profile_image` is not null in the database
2. Verify the URL/path is correct
3. Make sure the image URL is publicly accessible
4. Check browser console for errors (F12 → Console tab)

---

## Image Optimization Tips

### Before Uploading

1. **Resize to 400x400 pixels** - Use tools like:
   - https://squoosh.app (online, free)
   - https://tinypng.com (compress images)
   - Photoshop, GIMP, or Paint.NET

2. **Optimize file size:**
   - Target: 100-300KB
   - Format: WebP (best), JPEG (good), PNG (if transparency needed)

3. **Make it professional:**
   - Good lighting
   - Neutral background
   - Professional attire (if appropriate)
   - Friendly expression
   - Head and shoulders visible

---

## Where Your Picture Appears

Your profile picture is displayed in:

1. **Hero Section** (top of the page)
   - Large circular image
   - Gradient border effect
   - Animated on hover

2. **About Section** (if you enable it)
   - Can be displayed next to bio

3. **Favicon** (optional)
   - Can be used as site icon

---

## Example: Complete Update

Here's a complete example of updating your profile with a picture:

```bash
# Start backend
cd backend
python run.py

# In another terminal, update your profile
curl -X PATCH http://localhost:8000/api/v1/profile/1 \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Wandile Nene",
    "title": "Full Stack Developer",
    "profile_image": "https://avatars.githubusercontent.com/u/12345678",
    "bio": "Passionate developer building amazing web applications"
  }'

# Refresh http://localhost:5173 to see changes
```

---

## Recommended Hosting Services (Free)

If you don't have an image URL, use one of these free services:

| Service | URL | Notes |
|---------|-----|-------|
| **Imgur** | imgur.com | Easy, reliable, no account needed |
| **GitHub** | github.com | Use your GitHub avatar |
| **LinkedIn** | linkedin.com | Use your LinkedIn photo |
| **Cloudinary** | cloudinary.com | Free tier, CDN, image optimization |
| **ImageKit** | imagekit.io | Free tier, fast CDN |

**Tip:** Imgur is the easiest for testing!

---

## Production Considerations

For a deployed portfolio:

1. ✅ **Use a CDN** (Cloudinary, ImageKit)
2. ✅ **Optimize images** (WebP format)
3. ✅ **Use HTTPS URLs** (secure)
4. ✅ **Add alt text** (already included)
5. ✅ **Serve multiple sizes** (responsive images)
6. ✅ **Enable caching** (fast loading)

---

## Next Steps

1. **Choose a method** (URL, local file, or upload)
2. **Get your image ready** (400x400px, optimized)
3. **Update your profile** (use API or Postman)
4. **Refresh your browser** (see your picture!)
5. **Test in both themes** (dark and light mode)

---

## Quick Reference

```bash
# View current profile
curl http://localhost:8000/api/v1/profile/1

# Update profile picture (URL)
curl -X PATCH http://localhost:8000/api/v1/profile/1 \
  -H "Content-Type: application/json" \
  -d '{"profile_image": "YOUR_URL_HERE"}'

# Update profile picture (local)
curl -X PATCH http://localhost:8000/api/v1/profile/1 \
  -H "Content-Type: application/json" \
  -d '{"profile_image": "/images/profile.jpg"}'
```

---

## Need Help?

- **Can't see changes?** → Clear browser cache (Ctrl+Shift+R)
- **Image broken?** → Check URL is publicly accessible
- **Wrong size?** → CSS will auto-resize, but 400x400px is ideal
- **Want to change it?** → Just run the update command again!

**That's it!** Your profile picture should now be displayed beautifully in your portfolio! 🎉
