# Web Deployment Guide - No CLI Required

## Option 1: Vercel (Recommended)

### Step-by-Step Instructions:

1. **Upload to GitHub**
   - Create a new repository on GitHub
   - Upload all your project files
   - Make sure `vercel.json` and `requirements.txt` are included

2. **Deploy via Vercel Website**
   - Visit [vercel.com](https://vercel.com)
   - Click "Continue with GitHub"
   - Click "New Project"
   - Select your repository
   - Vercel auto-detects Python projects

3. **Set Environment Variables**
   - In project settings, add environment variables:
     ```
     GEMINI_API_KEY = your_actual_api_key_here
     SECRET_KEY = any_secure_random_string
     ```
   - **Important**: Set these in Vercel dashboard, not in code

4. **Deploy**
   - Click "Deploy"
   - Wait for build to complete
   - Your app will be live at: `https://your-project.vercel.app`

## Environment Variables Setup in Vercel Dashboard

1. Go to your project dashboard on Vercel
2. Click on "Settings" tab
3. Click on "Environment Variables" in the sidebar
4. Add these variables:
   - Name: `GEMINI_API_KEY`, Value: `your_actual_gemini_api_key`
   - Name: `SECRET_KEY`, Value: `any_secure_random_string_here`

## Troubleshooting Common Issues

### "functions property cannot be used with builds"
- ✅ Fixed: Removed conflicting `functions` property from vercel.json

### Build Fails
- Check that all required files are uploaded to GitHub
- Verify requirements.txt contains correct dependencies
- Make sure Python version is compatible (3.9 recommended)

### 500 Errors After Deployment
- Verify GEMINI_API_KEY is set correctly in Vercel dashboard
- Check function logs in Vercel dashboard for detailed errors
- Ensure all import statements work with the simplified file structure

### API Timeouts
- Vercel has a 60-second timeout limit for serverless functions
- Some AI operations may take time - this is normal for the first request

## Testing Your Deployment

1. **Health Check**: Visit `https://your-app.vercel.app/health`
2. **Main Dashboard**: Visit `https://your-app.vercel.app/`
3. **Test Analysis**: Try analyzing a sample policy clause

## Success Indicators
✅ Health endpoint returns `{"status": "healthy"}`
✅ Main dashboard loads without errors
✅ Policy analysis feature works
✅ No GEMINI_API_KEY errors in Vercel function logs

## Quick Test Clause
Use this sample clause to test your deployment:
```
"The insurer shall provide coverage for losses occurring during the policy period, subject to the terms and conditions specified herein."
```

Your PolicyIntelliHub should analyze this and provide all 7 AI agent results!
✅ Health endpoint returns "healthy"
✅ Main dashboard loads
✅ Policy analysis works
✅ No API key errors in logs
