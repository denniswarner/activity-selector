# Deployment Guide

This guide will help you deploy your Activity Selector application to production.

## Overview

- **Frontend**: Deploy to Vercel (React + Vite)
- **Backend**: Deploy to Railway/Render/Heroku (FastAPI)

## Frontend Deployment (Vercel)

### Prerequisites
- Vercel account (free at [vercel.com](https://vercel.com))
- GitHub repository with your code

### Steps

1. **Push your code to GitHub** (if not already done):
   ```bash
   git add .
   git commit -m "Add Vercel configuration"
   git push origin main
   ```

2. **Deploy to Vercel**:
   - Go to [vercel.com](https://vercel.com) and sign in
   - Click "New Project"
   - Import your GitHub repository
   - Set the following configuration:
     - **Framework Preset**: Vite
     - **Root Directory**: `frontend`
     - **Build Command**: `npm run build`
     - **Output Directory**: `dist`
     - **Install Command**: `npm install`

3. **Environment Variables**:
   Add these in Vercel project settings:
   ```
   VITE_API_URL=https://your-backend-url.com
   ```

4. **Deploy**:
   - Click "Deploy"
   - Vercel will automatically build and deploy your frontend

## Backend Deployment Options (Free)

### Option 1: Render (Recommended - Free Tier)

1. **Create Render account** at [render.com](https://render.com)
2. **Create new Web Service**:
   - Connect your GitHub repository
   - Set root directory to `backend`
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free (750 hours/month)
3. **Environment Variables**:
   ```
   GOOGLE_SHEETS_CREDENTIALS_FILE=your-credentials-content
   SPREADSHEET_ID=your-spreadsheet-id
   ```
4. **Deploy**: Render will build and deploy automatically

**Free Tier Limits:**
- 750 hours/month (enough for 24/7 uptime)
- Sleeps after 15 minutes of inactivity
- 512MB RAM
- Shared CPU

### Option 2: Fly.io (Free Tier)

1. **Install Fly CLI**:
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```
2. **Sign up** at [fly.io](https://fly.io)
3. **Create app**:
   ```bash
   cd backend
   fly launch
   ```
4. **Deploy**:
   ```bash
   fly deploy
   ```
5. **Set secrets**:
   ```bash
   fly secrets set GOOGLE_SHEETS_CREDENTIALS_FILE="your-credentials"
   fly secrets set SPREADSHEET_ID="your-spreadsheet-id"
   ```

**Free Tier Limits:**
- 3 shared-cpu-1x 256mb VMs
- 3GB persistent volume storage
- 160GB outbound data transfer

### Option 3: Railway (Limited Free)

1. **Create Railway account** at [railway.app](https://railway.app)
2. **Connect your GitHub repository**
3. **Create new service**:
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Set root directory to `backend`
4. **Environment Variables**: Same as above
5. **Deploy**: Railway will automatically detect Python and deploy

**Free Tier Limits:**
- $5 credit/month
- Sleeps after inactivity
- Good for development/testing

### Option 4: PythonAnywhere (Free Tier)

1. **Create account** at [pythonanywhere.com](https://pythonanywhere.com)
2. **Upload your code** via Git or file upload
3. **Set up virtual environment**:
   ```bash
   mkvirtualenv --python=/usr/bin/python3.9 myenv
   pip install -r requirements.txt
   ```
4. **Configure WSGI file** for FastAPI
5. **Set environment variables** in the web app settings

**Free Tier Limits:**
- 512MB storage
- Limited CPU time
- Custom domains not supported
- Good for simple apps

### Option 5: Heroku (Limited Free)

**Note**: Heroku discontinued their free tier, but they offer a basic paid plan ($5/month).

1. **Create Heroku account** and install CLI
2. **Create new app**:
   ```bash
   heroku create your-app-name
   ```
3. **Set buildpacks**:
   ```bash
   heroku buildpacks:set heroku/python
   ```
4. **Deploy**:
   ```bash
   git subtree push --prefix backend heroku main
   ```
5. **Set environment variables**:
   ```bash
   heroku config:set GOOGLE_SHEETS_CREDENTIALS_FILE="your-credentials"
   heroku config:set SPREADSHEET_ID="your-spreadsheet-id"
   ```

## Google Sheets Setup for Production

### 1. Service Account Setup
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project or select existing
3. Enable Google Sheets API
4. Create a service account
5. Download the JSON credentials file

### 2. Share Your Sheet
- Share your Google Sheet with the service account email
- Give it "Editor" permissions

### 3. Environment Variables
For production, you'll need to set these environment variables:

**Railway/Render/Heroku:**
```
GOOGLE_SHEETS_CREDENTIALS_FILE={"type":"service_account","project_id":"...","private_key_id":"...","private_key":"...","client_email":"...","client_id":"...","auth_uri":"...","token_uri":"...","auth_provider_x509_cert_url":"...","client_x509_cert_url":"..."}
SPREADSHEET_ID=your-spreadsheet-id-here
```

## Post-Deployment

### 1. Update Frontend API URL
Once your backend is deployed, update the `VITE_API_URL` in Vercel to point to your backend URL.

### 2. Test Your Application
- Test all API endpoints
- Verify Google Sheets integration
- Check CORS settings

### 3. Custom Domain (Optional)
- Add custom domain in Vercel settings
- Update DNS records as instructed

## Troubleshooting

### Common Issues

1. **CORS Errors**:
   - Ensure backend CORS settings include your frontend domain
   - Check that preflight requests are handled

2. **Google Sheets Access**:
   - Verify service account has access to the sheet
   - Check credentials format in environment variables

3. **Build Failures**:
   - Check build logs in deployment platform
   - Verify all dependencies are in requirements.txt

4. **Environment Variables**:
   - Ensure all required variables are set
   - Check variable names match exactly

### Debugging

1. **Check Logs**:
   - Vercel: Project dashboard → Functions → View logs
   - Railway: Service → Logs tab
   - Render: Service → Logs tab

2. **Test Locally**:
   - Test with production environment variables locally
   - Verify API endpoints work with deployed backend

## Security Considerations

1. **Environment Variables**:
   - Never commit credentials to Git
   - Use platform-specific secret management

2. **CORS**:
   - Restrict CORS origins to your frontend domain
   - Don't use wildcard (*) in production

3. **API Security**:
   - Consider adding authentication for production use
   - Rate limiting for API endpoints

## Monitoring

1. **Vercel Analytics**: Built-in performance monitoring
2. **Backend Monitoring**: Use platform-specific tools
3. **Error Tracking**: Consider Sentry for error monitoring

## Cost Optimization

### Free Tier Options:
- **Vercel**: Free tier includes 100GB bandwidth/month
- **Render**: Free tier includes 750 hours/month (enough for 24/7)
- **Fly.io**: Free tier includes 3 VMs and 160GB transfer
- **Railway**: Free tier includes $5 credit/month
- **PythonAnywhere**: Free tier for simple apps

### Recommended Free Stack:
1. **Frontend**: Vercel (always free)
2. **Backend**: Render (750 hours/month free)
3. **Total Cost**: $0/month

### When to Upgrade:
- **Render**: If you need more than 750 hours/month ($7/month)
- **Fly.io**: If you need more resources ($1.94/month per VM)
- **Railway**: If you need more than $5 credit/month

---

Your application should now be live and accessible from anywhere! 🚀 