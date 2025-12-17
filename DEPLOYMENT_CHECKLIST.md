# Deployment Checklist

Complete checklist for deploying LibreTranslate with separate frontend/backend servers.

## Pre-Deployment

### Backend Server (`api.shravani.group`)

- [ ] Server provisioned and accessible
- [ ] Domain DNS configured: `api.shravani.group` → Server IP
- [ ] SSL certificate ready (Let's Encrypt recommended)
- [ ] Docker/Coolify installed (if using)
- [ ] Persistent volume configured for models
- [ ] Environment variables prepared

### Frontend Server (`translate.shravani.group`)

- [ ] Server provisioned and accessible
- [ ] Domain DNS configured: `translate.shravani.group` → Server IP
- [ ] SSL certificate ready (Let's Encrypt recommended)
- [ ] Web server installed (Nginx/Apache) OR Node.js installed
- [ ] Frontend files ready in repository

## Backend Deployment

### Step 1: Deploy Backend API

- [ ] Clone/pull repository to server
- [ ] Set up environment variables:
  ```
  CORS_ORIGINS=https://translate.shravani.group
  HOST=0.0.0.0
  PORT=3000
  AUTO_INSTALL_MODELS=true
  ```
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Start server (or deploy via Coolify/Docker)
- [ ] Verify server is running: `curl http://localhost:3000/`

### Step 2: Configure Domain & SSL

- [ ] Point `api.shravani.group` to server IP
- [ ] Obtain SSL certificate:
  ```bash
  certbot certonly --nginx -d api.shravani.group
  ```
- [ ] Configure reverse proxy (Nginx/Apache) if needed
- [ ] Test: `curl https://api.shravani.group/`

### Step 3: Verify Backend

- [ ] Health check: `curl https://api.shravani.group/health`
- [ ] Languages endpoint: `curl https://api.shravani.group/languages`
- [ ] API docs: Visit `https://api.shravani.group/docs`
- [ ] Check CORS headers in response
- [ ] Verify models are installed (check logs)

## Frontend Deployment

### Step 1: Deploy Frontend Files

**Option A: Nginx/Apache**
- [ ] Copy frontend files to web server directory:
  ```bash
  sudo cp -r frontend/* /var/www/translate.shravani.group/
  ```
- [ ] Set permissions:
  ```bash
  sudo chown -R www-data:www-data /var/www/translate.shravani.group
  sudo chmod -R 755 /var/www/translate.shravani.group
  ```

**Option B: Node.js Server**
- [ ] Copy frontend directory to server
- [ ] Install dependencies: `npm install`
- [ ] Start server: `npm start` or use PM2
- [ ] Configure process manager (PM2/systemd)

**Option C: Static Hosting (Cloudflare Pages, Vercel, Netlify)**
- [ ] Connect repository
- [ ] Set build directory to `frontend/`
- [ ] Deploy

### Step 2: Configure Web Server

**Nginx:**
- [ ] Copy `frontend/nginx.conf.example` to `/etc/nginx/sites-available/translate.shravani.group`
- [ ] Update paths in config file
- [ ] Enable site: `sudo ln -s /etc/nginx/sites-available/translate.shravani.group /etc/nginx/sites-enabled/`
- [ ] Test config: `sudo nginx -t`
- [ ] Reload: `sudo systemctl reload nginx`

**Apache:**
- [ ] Copy `frontend/apache.conf.example` to `/etc/apache2/sites-available/translate.shravani.group.conf`
- [ ] Update paths in config file
- [ ] Enable site: `sudo a2ensite translate.shravani.group.conf`
- [ ] Enable required modules: `sudo a2enmod ssl rewrite headers`
- [ ] Reload: `sudo systemctl reload apache2`

### Step 3: Configure Domain & SSL

- [ ] Point `translate.shravani.group` to server IP
- [ ] Obtain SSL certificate:
  ```bash
  certbot certonly --nginx -d translate.shravani.group
  # or
  certbot certonly --apache -d translate.shravani.group
  ```
- [ ] Update web server config with SSL paths
- [ ] Test: `curl https://translate.shravani.group/`

### Step 4: Verify Frontend

- [ ] Visit `https://translate.shravani.group/` in browser
- [ ] Check browser console for errors
- [ ] Verify API calls go to `api.shravani.group`
- [ ] Test translation functionality
- [ ] Test authentication (signup/login)

## Integration Testing

### API Connectivity

- [ ] Frontend can reach backend API
- [ ] No CORS errors in browser console
- [ ] API responses include proper CORS headers
- [ ] Authentication requests work
- [ ] Translation requests work

### Functionality Testing

- [ ] User signup works
- [ ] User login works
- [ ] Translation works
- [ ] Language detection works
- [ ] Usage tracking works
- [ ] Plan upgrade works (if implemented)
- [ ] Dashboard displays correctly

### Performance Testing

- [ ] Page load time < 2 seconds
- [ ] Translation response time < 1 second
- [ ] Static assets cached properly
- [ ] Gzip compression enabled
- [ ] SSL/TLS working correctly

## Security Checklist

### Backend Security

- [ ] API key authentication configured (if needed)
- [ ] CORS restricted to frontend domain only
- [ ] SSL/TLS enabled
- [ ] Rate limiting configured (if needed)
- [ ] User passwords hashed
- [ ] JWT tokens expire properly
- [ ] Environment variables secured
- [ ] Logs don't contain sensitive data

### Frontend Security

- [ ] HTTPS enforced
- [ ] Security headers configured (X-Frame-Options, CSP, etc.)
- [ ] No sensitive data in client-side code
- [ ] API keys not exposed (if using)
- [ ] Input validation on forms
- [ ] XSS protection enabled

## Monitoring & Maintenance

### Logging

- [ ] Backend logs configured
- [ ] Frontend access logs configured
- [ ] Error logs monitored
- [ ] Log rotation configured

### Monitoring

- [ ] Server uptime monitoring
- [ ] API response time monitoring
- [ ] Error rate monitoring
- [ ] Usage statistics tracking
- [ ] SSL certificate expiration alerts

### Backup

- [ ] User data backed up (`users.json` or database)
- [ ] Model files backed up (if custom)
- [ ] Configuration files backed up
- [ ] Backup schedule configured

## Post-Deployment

### Documentation

- [ ] Update DNS records documented
- [ ] Server credentials secured
- [ ] Deployment process documented
- [ ] Rollback procedure documented
- [ ] Contact information for issues

### Communication

- [ ] Users notified of new service
- [ ] Support channels established
- [ ] Documentation published
- [ ] API documentation accessible

## Troubleshooting

### Common Issues

**CORS Errors:**
- [ ] Check `CORS_ORIGINS` environment variable
- [ ] Verify exact domain match (including https://)
- [ ] Check browser console for exact error
- [ ] Test with `curl -H "Origin: https://translate.shravani.group" ...`

**API Not Found:**
- [ ] Verify backend is running
- [ ] Check API URL in frontend JavaScript
- [ ] Test API directly with curl
- [ ] Check reverse proxy configuration

**Frontend Not Loading:**
- [ ] Verify files are in correct directory
- [ ] Check file permissions
- [ ] Check web server configuration
- [ ] Check browser console for errors
- [ ] Verify SSL certificate is valid

**Translation Not Working:**
- [ ] Check models are installed
- [ ] Verify translation service initialized
- [ ] Check backend logs for errors
- [ ] Test API endpoint directly

## Quick Verification Commands

```bash
# Backend health
curl https://api.shravani.group/health

# Backend languages
curl https://api.shravani.group/languages

# Frontend accessibility
curl -I https://translate.shravani.group/

# CORS test
curl -H "Origin: https://translate.shravani.group" \
     -H "Access-Control-Request-Method: POST" \
     -H "Access-Control-Request-Headers: Content-Type" \
     -X OPTIONS \
     https://api.shravani.group/translate

# SSL certificate check
openssl s_client -connect api.shravani.group:443 -servername api.shravani.group
openssl s_client -connect translate.shravani.group:443 -servername translate.shravani.group
```

## Success Criteria

✅ Frontend accessible at `https://translate.shravani.group/`  
✅ Backend API accessible at `https://api.shravani.group/`  
✅ No CORS errors  
✅ Translation works end-to-end  
✅ Authentication works  
✅ SSL certificates valid  
✅ Performance acceptable  
✅ Security measures in place  

---

**Last Updated:** December 2024  
**Maintained By:** Development Team

