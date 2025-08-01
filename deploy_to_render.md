# 🚀 Direct Deployment to Render.com (No Git Required)

## **Step 1: Create Render Account**
1. Go to [render.com](https://render.com)
2. Click "Get Started for Free"
3. Sign up with your email or GitHub account

## **Step 2: Create New Web Service**
1. In your Render dashboard, click "New +"
2. Select "Web Service"
3. Choose "Build and deploy from a Git repository"

## **Step 3: Connect Repository**
1. **If you have GitHub:**
   - Connect your GitHub account
   - Select your repository
   
2. **If you don't have GitHub:**
   - Create a free GitHub account
   - Upload your files to GitHub (see instructions below)

## **Step 4: Configure Deployment**
Set these settings in Render:

- **Name:** `osint-app` (or any name you prefer)
- **Environment:** `Python 3`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn app:app`
- **Plan:** Free

## **Step 5: Environment Variables (Optional)**
Add these in the "Environment" tab:

```
OPENAI_API_KEY=your_openai_key_here
GEMINI_API_KEY=your_gemini_key_here
SHODAN_API_KEY=your_shodan_key_here
NUMVERIFY_API_KEY=your_numverify_key_here
```

## **Step 6: Deploy**
1. Click "Create Web Service"
2. Wait for build to complete (5-10 minutes)
3. Your app will be available at: `https://your-app-name.onrender.com`

---

## **Quick GitHub Setup (if needed):**

### **Option 1: GitHub Desktop**
1. Download [GitHub Desktop](https://desktop.github.com/)
2. Install and sign in
3. Click "Clone a repository from the Internet"
4. Create new repository
5. Copy your files to the repository folder
6. Commit and push

### **Option 2: GitHub Web Interface**
1. Go to github.com and create account
2. Create new repository
3. Upload files using web interface
4. Copy repository URL for Render

---

## **Troubleshooting:**

### **Common Issues:**
- **Build fails:** Check that all files are uploaded
- **App crashes:** Check logs in Render dashboard
- **API errors:** Verify environment variables are set correctly

### **Files Required:**
- ✅ `app.py` (main application)
- ✅ `requirements.txt` (dependencies)
- ✅ `Procfile` (deployment config)
- ✅ `runtime.txt` (Python version)
- ✅ `templates/` folder (HTML templates)

### **Success Indicators:**
- Build completes without errors
- App shows "Deploy successful"
- You can access your app URL
- All OSINT tools work properly

---

**Your app will be live at:** `https://your-app-name.onrender.com` 