# DeepShield Troubleshooting Guide

## Common Installation Issues

### Backend

#### MongoDB Connection Issues
```
Error: MongoDB connection failed
```

**Solution:**
1. Verify MongoDB is running:
```bash
sudo systemctl status mongodb
```
2. Check MongoDB URL in `.env`
3. Ensure MongoDB is listening on the correct port:
```bash
netstat -plntu | grep 27017
```

#### Python Dependencies
```
Error: No module named 'fastapi'
```

**Solution:**
1. Verify virtual environment is activated
2. Reinstall dependencies:
```bash
pip install -r requirements.txt --no-cache-dir
```

#### AI Model Loading Errors
```
Error: Failed to load model
```

**Solution:**
1. Check internet connection (models are downloaded on first use)
2. Verify model files in data/datasets directory
3. Clear model cache and retry:
```bash
rm -rf ~/.cache/torch/hub/
```

### Frontend

#### Node.js Version Conflicts
```
Error: The engine "node" is incompatible with this module
```

**Solution:**
1. Install correct Node.js version:
```bash
nvm install 18
nvm use 18
```
2. Clear npm cache:
```bash
npm cache clean --force
```

#### API Connection Issues
```
Error: Failed to fetch API endpoint
```

**Solution:**
1. Verify backend is running
2. Check VITE_API_URL in frontend .env
3. Ensure CORS is properly configured
4. Check browser console for specific errors

## Runtime Issues

### Deepfake Detection

#### Slow Analysis
**Problem:** Media analysis taking too long

**Solution:**
1. Check media file size (recommend < 10MB)
2. Verify system resources
3. Consider enabling GPU acceleration

#### False Positives
**Problem:** Incorrect deepfake detection

**Solution:**
1. Update model confidence threshold in config
2. Verify image quality
3. Try different analysis algorithms

### Content Moderation

#### Language Detection Issues
**Problem:** Incorrect language detection

**Solution:**
1. Verify text length (minimum 10 characters)
2. Check supported languages list
3. Update language detection threshold

#### Memory Issues
```
Error: Out of memory
```

**Solution:**
1. Reduce batch size in config
2. Implement pagination for large datasets
3. Monitor system resources

### Instagram Integration

#### Webhook Verification Fails
**Problem:** Instagram webhook verification failing

**Solution:**
1. Verify webhook URL is publicly accessible
2. Check webhook secret in config
3. Validate signature calculation
4. Review Instagram app settings

#### Media Processing Errors
**Problem:** Failed to process Instagram media

**Solution:**
1. Verify Instagram access token
2. Check media permissions
3. Review API quota limits
4. Ensure media URL is accessible

## Performance Optimization

### Backend
1. Enable caching for frequent requests
2. Implement database indexing
3. Use asynchronous processing for heavy tasks
4. Monitor memory usage

### Frontend
1. Enable code splitting
2. Implement lazy loading
3. Optimize image loading
4. Use production builds

## Security Issues

### Authentication Failures
**Problem:** Unable to login/register

**Solution:**
1. Clear browser cache
2. Verify JWT secret in config
3. Check token expiration
4. Review security logs

### API Access Issues
**Problem:** Unauthorized API access

**Solution:**
1. Verify token in requests
2. Check user permissions
3. Review API security settings
4. Monitor access logs

## Monitoring and Logging

### Access Logs
Location: `/var/log/deepshield/access.log`
- Contains API access information
- User authentication attempts
- Request/response details

### Error Logs
Location: `/var/log/deepshield/error.log`
- Application errors
- System warnings
- Performance issues

### Monitoring Tools
1. Use Prometheus for metrics
2. Set up Grafana dashboards
3. Configure email alerts
4. Monitor system resources

## Getting Help

If you encounter issues not covered in this guide:
 
1. Check the latest documentation
2. Review GitHub issues
3. Contact support team
4. Join developer community
