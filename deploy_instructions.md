# Manual Deployment Instructions for Render.com

## Quick Fix for "Not Found" Error

The app has been updated with the following fixes:

1. **Explicit Flask Configuration**: Added explicit template and static folder paths
2. **Improved Fallback**: Better error handling for template loading
3. **Debug Route**: Added `/debug` endpoint to troubleshoot issues

## To Deploy These Changes:

### Option 1: Using GitHub Desktop (Recommended)
1. Open GitHub Desktop
2. Navigate to your OSINT repository
3. You should see the changes in the "Changes" tab
4. Add a commit message like: "Fix template loading and add debug route"
5. Click "Commit to main"
6. Click "Push origin" to push to GitHub
7. Render will automatically redeploy

### Option 2: Manual File Upload
1. Go to your Render.com dashboard
2. Navigate to your OSINT service
3. Go to "Settings" tab
4. Scroll down to "Build & Deploy"
5. Click "Manual Deploy" → "Deploy latest commit"

### Option 3: Direct File Edit on Render
1. Go to your Render.com dashboard
2. Navigate to your OSINT service
3. Go to "Settings" tab
4. Scroll down to "Environment Variables"
5. Add a new environment variable:
   - Key: `FLASK_ENV`
   - Value: `production`

## After Deployment:

1. **Test the main URL**: Your app should now load properly
2. **Test the debug route**: Visit `your-app-url/debug` to see configuration info
3. **Check logs**: If issues persist, check the logs in Render dashboard

## Expected Results:

- ✅ Main page loads without "Not Found" error
- ✅ `/debug` route shows template configuration
- ✅ All OSINT tools work properly

## If Issues Persist:

1. Check the `/debug` route output
2. Review Render logs for specific error messages
3. Ensure all files are properly committed to GitHub 