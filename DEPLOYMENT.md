# QuickCred Deployment Guide

This guide covers different deployment options for the QuickCred micro-lending platform.

## 🚀 Quick Start

### Local Development
```bash
# 1. Run setup script
python setup.py

# 2. Create demo data
python demo_data.py

# 3. Start development server
python run.py
```

## ☁️ Cloud Deployment Options

### 1. Render (Recommended for Flask)

#### Prerequisites
- GitHub repository
- MongoDB Atlas account
- Render account

#### Steps
1. **Connect Repository**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

2. **Configure Service**
   ```
   Name: quickcred
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: python app.py
   ```

3. **Set Environment Variables**
   ```
   SECRET_KEY=your-production-secret-key
   JWT_SECRET_KEY=your-production-jwt-key
   MONGO_URI=your-mongodb-atlas-connection-string
   ```

4. **Deploy**
   - Click "Create Web Service"
   - Render will automatically build and deploy

#### Render Configuration File
Create `render.yaml` in your repository root:
```yaml
services:
  - type: web
    name: quickcred
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python app.py
    envVars:
      - key: SECRET_KEY
        generateValue: true
      - key: JWT_SECRET_KEY
        generateValue: true
      - key: MONGO_URI
        sync: false
```

### 2. Heroku

#### Prerequisites
- Heroku CLI installed
- Git repository
- MongoDB Atlas account

#### Steps
1. **Create Heroku App**
   ```bash
   heroku create quickcred-app
   ```

2. **Set Environment Variables**
   ```bash
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set JWT_SECRET_KEY=your-jwt-key
   heroku config:set MONGO_URI=your-mongodb-uri
   ```

3. **Create Procfile**
   ```
   web: python app.py
   ```

4. **Deploy**
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

### 3. Railway

#### Steps
1. **Connect Repository**
   - Go to [Railway](https://railway.app)
   - Connect your GitHub repository

2. **Configure Environment**
   - Add environment variables in Railway dashboard
   - Set Python version to 3.8+

3. **Deploy**
   - Railway automatically detects Flask app
   - Deploys on push to main branch

### 4. DigitalOcean App Platform

#### Steps
1. **Create App**
   - Go to DigitalOcean App Platform
   - Create new app from GitHub

2. **Configure**
   ```
   Source: GitHub Repository
   Type: Web Service
   Build Command: pip install -r requirements.txt
   Run Command: python app.py
   ```

3. **Environment Variables**
   - Add all required environment variables
   - Set Python version to 3.8+

## 🗄️ Database Setup

### MongoDB Atlas (Recommended)

1. **Create Cluster**
   - Go to [MongoDB Atlas](https://cloud.mongodb.com)
   - Create a new cluster (M0 free tier available)

2. **Configure Access**
   - Create database user
   - Whitelist IP addresses (0.0.0.0/0 for all IPs)

3. **Get Connection String**
   ```
   mongodb+srv://username:password@cluster.mongodb.net/quickcred?retryWrites=true&w=majority
   ```

### Local MongoDB (Development Only)

```bash
# Install MongoDB locally
# Update MONGO_URI in .env
MONGO_URI=mongodb://localhost:27017/quickcred
```

## 🔧 Production Configuration

### Environment Variables
```env
# Production settings
SECRET_KEY=your-super-secure-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
MONGO_URI=your-mongodb-atlas-connection-string

# Optional: Flask settings
FLASK_ENV=production
FLASK_DEBUG=False
```

### Security Considerations
1. **Use Strong Secrets**: Generate random strings for SECRET_KEY and JWT_SECRET_KEY
2. **HTTPS Only**: Ensure your deployment uses HTTPS
3. **Database Security**: Use MongoDB Atlas with proper access controls
4. **Environment Variables**: Never commit secrets to version control

### Performance Optimization
1. **Database Indexing**: Add indexes for frequently queried fields
2. **Connection Pooling**: Configure MongoDB connection pooling
3. **Caching**: Implement Redis for session storage
4. **CDN**: Use CloudFlare or similar for static assets

## 📊 Monitoring & Analytics

### Health Checks
Add to your app:
```python
@app.route('/health')
def health_check():
    return {'status': 'healthy', 'timestamp': datetime.utcnow()}
```

### Logging
```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

### Error Tracking
Consider integrating:
- Sentry for error tracking
- New Relic for performance monitoring
- Google Analytics for user behavior

## 🔄 CI/CD Pipeline

### GitHub Actions Example
Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Deploy to Render
      uses: johnbeynon/render-deploy-action@v0.0.8
      with:
        service-id: ${{ secrets.RENDER_SERVICE_ID }}
        api-key: ${{ secrets.RENDER_API_KEY }}
```

## 🚨 Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Check MongoDB Atlas IP whitelist
   - Verify connection string format
   - Ensure database user has proper permissions

2. **Environment Variables Not Loading**
   - Check variable names (case-sensitive)
   - Restart application after changes
   - Verify .env file location

3. **Build Failures**
   - Check Python version compatibility
   - Verify all dependencies in requirements.txt
   - Check for missing system dependencies

4. **CORS Issues**
   - Configure CORS settings in Flask
   - Check domain whitelist
   - Verify HTTPS/HTTP protocol matching

### Debug Mode
For development, enable debug mode:
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

## 📈 Scaling Considerations

### Horizontal Scaling
- Use load balancers (nginx, HAProxy)
- Implement session storage (Redis)
- Database connection pooling

### Vertical Scaling
- Increase server resources
- Optimize database queries
- Implement caching strategies

### Database Scaling
- MongoDB Atlas auto-scaling
- Read replicas for analytics
- Sharding for large datasets

## 🔐 Security Checklist

- [ ] Strong secret keys
- [ ] HTTPS enabled
- [ ] Database access restricted
- [ ] Input validation implemented
- [ ] Rate limiting configured
- [ ] CORS properly configured
- [ ] Error messages sanitized
- [ ] Regular security updates

## 📞 Support

For deployment issues:
1. Check application logs
2. Verify environment variables
3. Test database connectivity
4. Review platform-specific documentation
5. Contact support team

---

**Happy Deploying! 🚀**
