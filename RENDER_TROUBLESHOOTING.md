# 🔧 Render.com Deployment Troubleshooting Guide

## **🚨 Common Error: "subprocess-exited-with-error"**

### **Problem:**
```
error: subprocess-exited-with-error
note: This error originates from a subprocess, and is likely not a problem with pip.
```

### **Root Causes:**
1. **Heavy Dependencies:** `opencv-python` and `moviepy` require system libraries
2. **Memory Limits:** Free tier has limited build memory
3. **Python Version Conflicts:** Incompatible package versions
4. **Missing System Dependencies:** Libraries not available in Render environment

---

## **✅ Solutions:**

### **Solution 1: Use Lightweight Requirements (Recommended)**
Replace your `requirements.txt` with:
```
Flask==2.3.3
Flask-CORS==4.0.0
requests==2.31.0
Pillow==10.0.1
numpy==1.24.3
gunicorn==21.2.0
```

### **Solution 2: Alternative Packages**
If you need video/image processing:
```
Flask==2.3.3
Flask-CORS==4.0.0
requests==2.31.0
Pillow==10.0.1
numpy==1.24.3
gunicorn==21.2.0
opencv-python-headless==4.8.1.78  # Lighter version
```

### **Solution 3: Build Configuration**
In Render dashboard, set:
- **Build Command:** `pip install -r requirements.txt --no-cache-dir`
- **Start Command:** `gunicorn app:app --timeout 120`

---

## **🔍 Debugging Steps:**

### **Step 1: Check Build Logs**
1. Go to your Render dashboard
2. Click on your service
3. Go to "Logs" tab
4. Look for specific error messages

### **Step 2: Test Locally**
```bash
# Test if requirements install locally
pip install -r requirements.txt
python app.py
```

### **Step 3: Verify Files**
Ensure these files are in your repository:
- ✅ `app.py`
- ✅ `requirements.txt`
- ✅ `Procfile`
- ✅ `runtime.txt`
- ✅ `templates/` folder

---

## **🛠️ Code Fixes:**

### **Fix 1: Handle Missing Packages Gracefully**
Your `app.py` now handles missing packages with try/except blocks.

### **Fix 2: Update Procfile**
Ensure your Procfile contains:
```
web: gunicorn app:app
```

### **Fix 3: Check Python Version**
Your `runtime.txt` should contain:
```
python-3.11.5
```

---

## **📋 Deployment Checklist:**

### **Before Deploying:**
- [ ] Remove heavy packages (`opencv-python`, `moviepy`)
- [ ] Test requirements locally
- [ ] Verify all files are committed
- [ ] Check Procfile syntax

### **During Deployment:**
- [ ] Monitor build logs
- [ ] Check for specific error messages
- [ ] Verify environment variables

### **After Deployment:**
- [ ] Test all endpoints
- [ ] Check app functionality
- [ ] Monitor performance

---

## **🚀 Quick Fix Commands:**

### **If Build Fails:**
1. **Update requirements.txt:**
   ```bash
   # Remove problematic packages
   pip uninstall opencv-python moviepy
   pip freeze > requirements.txt
   ```

2. **Force Rebuild:**
   - Go to Render dashboard
   - Click "Manual Deploy"
   - Select "Clear build cache & deploy"

3. **Check Environment:**
   - Verify Python version in `runtime.txt`
   - Check Procfile syntax
   - Ensure all files are committed

---

## **📊 Common Error Patterns:**

### **Pattern 1: Memory Issues**
```
error: subprocess-exited-with-error
```
**Fix:** Remove heavy packages, use lighter alternatives

### **Pattern 2: Version Conflicts**
```
ERROR: Could not find a version that satisfies the requirement
```
**Fix:** Update package versions, check compatibility

### **Pattern 3: System Dependencies**
```
error: command 'gcc' failed with exit status 1
```
**Fix:** Use pre-compiled packages or remove system-dependent packages

---

## **✅ Success Indicators:**

### **Build Success:**
- ✅ "Build completed successfully"
- ✅ No error messages in logs
- ✅ All packages installed correctly

### **Deployment Success:**
- ✅ "Deploy successful"
- ✅ App URL is accessible
- ✅ All features work properly

---

## **🆘 Emergency Fixes:**

### **If Nothing Works:**
1. **Create New Service:**
   - Delete current service
   - Create new web service
   - Use minimal requirements

2. **Use Alternative Platform:**
   - Railway.app (often more forgiving)
   - Heroku (paid but reliable)
   - PythonAnywhere (Python-focused)

3. **Simplify App:**
   - Remove video/image processing
   - Focus on core OSINT features
   - Add advanced features later

---

## **📞 Getting Help:**

### **Render Support:**
- Check Render documentation
- Contact Render support
- Use community forums

### **Debugging Tools:**
- Render build logs
- Local testing
- Package compatibility checkers

---

**🎯 Remember:** Start simple, add complexity gradually. Your OSINT app will work perfectly without the heavy video processing packages! 