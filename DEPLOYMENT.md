# 🚀 Deployment Guide

## Deploy to Render.com (Free & Recommended)

### Step 1: Prepare Your GitHub Repository

1. **Create a GitHub account** if you don't have one
2. **Create a new repository** named `fraud-detection-system`
3. **Upload all project files** to the repository

### Step 2: Deploy to Render.com

1. **Go to [Render.com](https://render.com)** and sign up with GitHub
2. **Click "New +"** and select "Web Service"
3. **Connect your GitHub repository**
4. **Configure the deployment:**

   ```
   Name: fraud-detection-system
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn app:app
   ```

5. **Set Environment Variables:**
   ```
   FLASK_ENV=production
   PORT=10000
   ```

6. **Click "Create Web Service"**

### Step 3: Access Your Live Application

- Your app will be available at: `https://your-app-name.onrender.com`
- Deployment takes 5-10 minutes
- Free tier includes 750 hours/month

## Alternative: Deploy to Heroku

### Prerequisites
- Heroku CLI installed
- Git installed

### Steps

1. **Login to Heroku**
   ```bash
   heroku login
   ```

2. **Create Heroku app**
   ```bash
   heroku create your-fraud-detection-app
   ```

3. **Deploy**
   ```bash
   git add .
   git commit -m "Deploy fraud detection system"
   git push heroku main
   ```

4. **Open your app**
   ```bash
   heroku open
   ```

## Environment Variables

For production deployment, set these environment variables:

```
FLASK_ENV=production
PORT=10000 (or as required by hosting platform)
```

## File Structure for Deployment

Ensure your project has these files:

```
fraud-detection-system/
├── app.py                 # Main Flask application
├── ml_pipeline.py         # Machine learning pipeline
├── requirements.txt       # Python dependencies
├── Procfile              # Process file for deployment
├── runtime.txt           # Python version specification
├── README.md             # Project documentation
├── .gitignore           # Git ignore file
├── templates/           # HTML templates
│   ├── base.html
│   ├── index.html
│   └── results.html
├── static/              # Static assets
│   ├── css/
│   ├── js/
│   └── images/
├── model/               # Trained ML models
│   ├── fraud_model.pkl
│   ├── scaler.pkl
│   └── feature_columns.pkl
└── uploads/             # Upload directory
    └── .gitkeep
```

## Troubleshooting

### Common Issues

1. **Build Fails**
   - Check `requirements.txt` for correct package versions
   - Ensure Python version in `runtime.txt` is supported

2. **App Crashes on Startup**
   - Check logs for model loading errors
   - Verify all model files are included in repository

3. **File Upload Issues**
   - Ensure `uploads/` directory exists
   - Check file size limits (usually 100MB max)

### Checking Logs

**Render.com:**
- Go to your service dashboard
- Click on "Logs" tab

**Heroku:**
```bash
heroku logs --tail
```

## Performance Optimization

### For Production

1. **Enable Gunicorn workers**
   ```
   web: gunicorn --workers=4 app:app
   ```

2. **Add caching headers**
   ```python
   @app.after_request
   def after_request(response):
       response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
       return response
   ```

3. **Optimize model loading**
   - Load models once at startup
   - Use model caching

## Security Considerations

1. **File Upload Security**
   - Validate file types
   - Limit file sizes
   - Scan for malicious content

2. **Environment Variables**
   - Never commit sensitive data
   - Use environment variables for secrets

3. **HTTPS**
   - Most platforms provide HTTPS by default
   - Ensure all external links use HTTPS

## Monitoring

### Health Checks

The app includes a health check endpoint:
```
GET /health
```

### Model Performance

Monitor these metrics:
- Response time
- Prediction accuracy
- Error rates
- Memory usage

## Scaling

### Free Tier Limitations

**Render.com:**
- 750 hours/month
- Sleeps after 15 minutes of inactivity
- 512MB RAM

**Heroku:**
- 550-1000 hours/month
- Sleeps after 30 minutes of inactivity
- 512MB RAM

### Upgrading

For production use, consider:
- Paid hosting plans
- Database integration
- Load balancing
- CDN for static assets

## Support

If you encounter issues:

1. Check the logs first
2. Verify all files are uploaded correctly
3. Test locally before deploying
4. Check platform-specific documentation

---

🎉 **Your fraud detection system is now live and accessible to everyone!**
