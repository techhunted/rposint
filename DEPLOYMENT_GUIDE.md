# 🚀 OSINT Web App Deployment Guide

## 📋 **Deployment Files Created:**
- ✅ `app.py` - Deployment-ready Flask application
- ✅ `requirements.txt` - Python dependencies
- ✅ `Procfile` - For Heroku/Render deployment
- ✅ `runtime.txt` - Python version specification

---

## 🌐 **Free Hosting Options:**

### **1. Render (Recommended - Free)**
**Best for beginners, easy setup, free tier available**

#### **Steps:**
1. **Create Render Account:**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub

2. **Connect Your Repository:**
   - Push your code to GitHub
   - Connect your GitHub repo to Render

3. **Deploy Settings:**
   ```
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn app:app
   Environment: Python 3.11
   ```

4. **Environment Variables (Optional):**
   ```
   OPENAI_API_KEY=your_openai_key
   GEMINI_API_KEY=your_gemini_key
   SHODAN_API_KEY=your_shodan_key
   ```

5. **Deploy:**
   - Click "Create New Service" → "Web Service"
   - Connect your GitHub repo
   - Render will automatically deploy your app

**✅ Pros:** Free tier, automatic deployments, custom domains
**❌ Cons:** Sleeps after 15 minutes of inactivity (free tier)

---

### **2. Railway (Free Tier)**
**Fast deployment, good performance**

#### **Steps:**
1. **Create Railway Account:**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

2. **Deploy:**
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway auto-detects Python and deploys

3. **Environment Variables:**
   - Go to "Variables" tab
   - Add your API keys

**✅ Pros:** Fast, reliable, good free tier
**❌ Cons:** Limited free tier usage

---

### **3. Heroku (Free Tier Discontinued)**
**Paid option, but very reliable**

#### **Steps:**
1. **Install Heroku CLI:**
   ```bash
   # Windows
   winget install --id=Heroku.HerokuCLI
   
   # Or download from: https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login and Deploy:**
   ```bash
   heroku login
   heroku create your-osint-app-name
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

3. **Set Environment Variables:**
   ```bash
   heroku config:set OPENAI_API_KEY=your_key
   heroku config:set GEMINI_API_KEY=your_key
   heroku config:set SHODAN_API_KEY=your_key
   ```

**✅ Pros:** Very reliable, great documentation
**❌ Cons:** No free tier anymore

---

### **4. PythonAnywhere (Free)**
**Good for Python apps, easy setup**

#### **Steps:**
1. **Create Account:**
   - Go to [pythonanywhere.com](https://pythonanywhere.com)
   - Sign up for free account

2. **Upload Files:**
   - Upload your files via Files tab
   - Or use Git: `git clone your-repo`

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure WSGI:**
   - Go to Web tab
   - Create new web app
   - Point to your `app.py`

**✅ Pros:** Python-focused, good free tier
**❌ Cons:** Limited resources on free tier

---

### **5. Vercel (Free)**
**Great for static sites, but requires adaptation**

#### **Steps:**
1. **Create Vercel Account:**
   - Go to [vercel.com](https://vercel.com)
   - Sign up with GitHub

2. **Deploy:**
   - Import your GitHub repo
   - Vercel will auto-detect and deploy

**✅ Pros:** Fast, great for static content
**❌ Cons:** Limited backend support

---

## 🔧 **Advanced Hosting Options:**

### **6. DigitalOcean App Platform**
**Professional hosting, reasonable pricing**

#### **Steps:**
1. **Create DigitalOcean Account:**
   - Go to [digitalocean.com](https://digitalocean.com)
   - Sign up (get $200 free credit)

2. **Deploy:**
   - Go to "Apps" → "Create App"
   - Connect your GitHub repo
   - Select Python environment

**✅ Pros:** Professional, reliable, good pricing
**❌ Cons:** Paid service

---

### **7. AWS Elastic Beanstalk**
**Enterprise-level hosting**

#### **Steps:**
1. **AWS Account:**
   - Create AWS account
   - Install AWS CLI

2. **Deploy:**
   ```bash
   eb init
   eb create osint-app
   eb deploy
   ```

**✅ Pros:** Scalable, enterprise features
**❌ Cons:** Complex setup, paid service

---

## 🛠️ **Pre-Deployment Checklist:**

### **✅ Files Ready:**
- [x] `app.py` - Main application
- [x] `requirements.txt` - Dependencies
- [x] `Procfile` - Process definition
- [x] `runtime.txt` - Python version
- [x] `templates/osint_app.html` - Frontend

### **✅ Code Changes Made:**
- [x] Removed `debug=True` for production
- [x] Added environment variable for port
- [x] Simplified video analysis for deployment
- [x] Added proper error handling

### **✅ API Keys (Optional):**
- [x] OpenAI API key configured
- [x] Gemini API key configured
- [x] Shodan API key configured
- [x] NumVerify API key configured

---

## 🚀 **Quick Start - Render (Recommended):**

### **Step 1: Prepare Your Code**
```bash
# Your files are already ready!
# Just push to GitHub
```

### **Step 2: Deploy to Render**
1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Configure:
   - **Name:** `osint-app`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
6. Click "Create Web Service"

### **Step 3: Set Environment Variables (Optional)**
1. Go to your service dashboard
2. Click "Environment" tab
3. Add your API keys:
   ```
   OPENAI_API_KEY=sk-...
   GEMINI_API_KEY=AIza...
   SHODAN_API_KEY=a72Q4g...
   ```

### **Step 4: Access Your App**
- Your app will be available at: `https://your-app-name.onrender.com`
- Render provides a free subdomain
- You can add custom domains later

---

## 🔍 **Testing Your Deployment:**

### **Local Testing:**
```bash
# Test locally first
python app.py
# Visit: http://localhost:5000
```

### **Online Testing:**
1. **Basic Functionality:**
   - Phone number analysis
   - Email analysis
   - Image upload
   - Website analysis

2. **API Testing:**
   - Test all endpoints
   - Check error handling
   - Verify file uploads

3. **Performance Testing:**
   - Load testing
   - Response times
   - Memory usage

---

## 🛡️ **Security Considerations:**

### **✅ Implemented:**
- [x] Input validation
- [x] File type checking
- [x] Error handling
- [x] CORS configuration

### **⚠️ Recommended:**
- [ ] Rate limiting
- [ ] API key rotation
- [ ] HTTPS enforcement
- [ ] Input sanitization
- [ ] File size limits

---

## 📊 **Monitoring & Maintenance:**

### **Health Checks:**
- Monitor response times
- Check error rates
- Monitor resource usage

### **Updates:**
- Keep dependencies updated
- Monitor security advisories
- Regular backups

---

## 🎯 **Recommended Deployment Order:**

1. **Start with Render** (Free, easy)
2. **Test thoroughly** on free tier
3. **Upgrade to paid** if needed
4. **Add custom domain** for production

---

## 📞 **Support & Troubleshooting:**

### **Common Issues:**
- **Build Failures:** Check `requirements.txt`
- **Runtime Errors:** Check logs
- **API Issues:** Verify environment variables
- **Performance:** Monitor resource usage

### **Getting Help:**
- Check deployment platform logs
- Review error messages
- Test locally first
- Use platform documentation

---

## 🎉 **Success!**

Once deployed, your OSINT web app will be available online with:
- ✅ All OSINT tools working
- ✅ AI analysis integration
- ✅ Shodan search capabilities
- ✅ File upload functionality
- ✅ Download results feature
- ✅ Mobile-responsive design

**Your app URL will be:** `https://your-app-name.onrender.com`

---

*Happy Deploying! 🚀* 