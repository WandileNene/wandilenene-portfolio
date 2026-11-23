# 📸 Add Your Photo - Quick Guide

## Three Simple Ways to Add Your Picture

### 🌐 Option 1: Use an Image URL (Fastest)

**If you have your photo online (LinkedIn, GitHub, etc.):**

1. **Get your image URL**:
   - Right-click your photo → "Copy image address"
   - You'll get something like: `https://avatars.githubusercontent.com/u/12345`

2. **Run this command** (replace with your URL):
   ```powershell
   # Windows PowerShell
   .\update_profile_picture.ps1 -ImageUrl "YOUR_IMAGE_URL_HERE"
   ```

3. **Refresh your browser** - Done! 🎉

---

### 📁 Option 2: Use a Local File (Recommended)

**If you have a photo file on your computer:**

1. **Copy your photo**:
   ```powershell
   # Create folder if it doesn't exist
   mkdir frontend\public\images -Force
   
   # Copy your photo (replace with your actual file path)
   copy "C:\path\to\your\photo.jpg" frontend\public\images\profile.jpg
   ```

2. **Update your profile**:
   ```powershell
   .\update_profile_picture.ps1 -ImageUrl "/images/profile.jpg"
   ```

3. **Refresh your browser** - Done! 🎉

---

### 🔗 Option 3: Use Imgur (If you don't have a URL)

**If your photo is only on your phone/computer:**

1. **Go to** https://imgur.com
2. **Upload your photo** (no account needed)
3. **Right-click the uploaded image** → "Copy image address"
4. **Run the command**:
   ```powershell
   .\update_profile_picture.ps1 -ImageUrl "YOUR_IMGUR_URL"
   ```

---

## Manual Method (Using API)

If you prefer to do it manually:

```bash
# 1. Start backend (if not running)
cd backend
python run.py

# 2. Update profile (in another terminal)
curl -X PATCH http://localhost:8000/api/v1/profile/1 \
  -H "Content-Type: application/json" \
  -d "{\"profile_image\": \"YOUR_URL_OR_PATH_HERE\"}"

# 3. Refresh browser
```

---

## Where Will My Photo Appear?

Your photo will be displayed in the **Hero section** (top of your portfolio) as a large circular profile picture with a gradient border effect.

---

## Recommended Image Specs

- ✅ **Size**: 400x400 pixels or larger
- ✅ **Format**: JPG, PNG, or WebP
- ✅ **Shape**: Square works best
- ✅ **File size**: Under 500KB
- ✅ **Quality**: High resolution, good lighting

---

## Quick Test

After updating, check if it worked:

```powershell
# View your current profile
curl http://localhost:8000/api/v1/profile/1 | Select-String profile_image
```

---

## Troubleshooting

**Photo not showing?**
1. Clear browser cache: Press `Ctrl + Shift + R`
2. Check backend is running: `http://localhost:8000`
3. Verify the image URL is publicly accessible
4. Check browser console for errors (F12)

**Need to change it?**
Just run the script again with a new URL!

---

## Examples

### Using GitHub Avatar
```powershell
.\update_profile_picture.ps1 -ImageUrl "https://avatars.githubusercontent.com/u/12345678"
```

### Using LinkedIn Photo
```powershell
.\update_profile_picture.ps1 -ImageUrl "https://media.licdn.com/dms/image/D4D03..."
```

### Using Local File
```powershell
# First copy your file
copy "C:\Users\YourName\Pictures\photo.jpg" frontend\public\images\profile.jpg

# Then update profile
.\update_profile_picture.ps1 -ImageUrl "/images/profile.jpg"
```

---

## 🎉 That's It!

**Choose any method above and your photo will appear in your portfolio!**

For detailed instructions, see [ADD_YOUR_PHOTO.md](./ADD_YOUR_PHOTO.md)
