# Separate Frontend/Backend Server Setup

This guide explains how to deploy the frontend and backend on separate servers.

## Architecture

```
┌─────────────────────────────────────┐
│   Frontend Server                    │
│   https://translate.shravani.group/  │
├─────────────────────────────────────┤
│  • Serves HTML/CSS/JS               │
│  • Makes API calls to backend       │
│  • Static files only                │
└─────────────────────────────────────┘
              │
              │ API Calls
              ▼
┌─────────────────────────────────────┐
│   Backend API Server                │
│   https://api.shravani.group/       │
├─────────────────────────────────────┤
│  • Translation API                  │
│  • Authentication API              │
│  • Subscription API                │
│  • CORS configured for frontend    │
└─────────────────────────────────────┘
```

## Backend Server Setup (API Only)

### 1. Configure CORS

Set the `CORS_ORIGINS` environment variable to allow your frontend domain:

**In Coolify (Backend Server):**
```
CORS_ORIGINS=https://translate.shravani.group
```

**Or in `.env` file:**
```bash
CORS_ORIGINS=https://translate.shravani.group
```

**For multiple origins (development + production):**
```
CORS_ORIGINS=https://translate.shravani.group,http://localhost:3000
```

### 2. Backend Endpoints

The backend API will be available at:
- `https://api.shravani.group/translate`
- `https://api.shravani.group/languages`
- `https://api.shravani.group/api/auth/login`
- `https://api.shravani.group/api/auth/signup`
- etc.

### 3. Verify Backend is API-Only

The backend no longer serves static files. The root endpoint (`/`) returns API information:

```json
{
  "message": "LibreTranslate API Server",
  "version": "1.0.0",
  "docs": "/docs",
  "frontend": "https://translate.shravani.group/"
}
```

## Frontend Server Setup

### 1. Update API URL

The frontend JavaScript automatically detects the API server URL:

**Production (translate.shravani.group):**
- Automatically uses: `https://api.shravani.group`

**Development (localhost):**
- Uses: `window.location.origin` (same server)

### 2. Manual API URL Configuration

If you need to override the API URL, edit `frontend/js/app.js`:

```javascript
const API_BASE_URL = 'https://api.shravani.group';  // Your API server
```

### 3. Deploy Frontend

#### Option A: Static File Hosting (Recommended)

Deploy the `frontend/` directory to:
- **Nginx** - Serve static files
- **Apache** - Serve static files
- **Cloudflare Pages** - Static site hosting
- **Vercel** - Static site hosting
- **Netlify** - Static site hosting
- **GitHub Pages** - Static site hosting

#### Option B: Separate Node.js/Express Server

Create a simple Express server to serve static files:

```javascript
// server.js
const express = require('express');
const path = require('path');
const app = express();

app.use(express.static(path.join(__dirname, 'frontend')));

app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'frontend', 'index.html'));
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Frontend server running on port ${PORT}`);
});
```

#### Option C: Nginx Configuration

```nginx
server {
    listen 80;
    server_name translate.shravani.group;

    root /path/to/frontend;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /static/ {
        alias /path/to/frontend/;
    }
}
```

## Deployment Steps

### Step 1: Deploy Backend API

1. **Deploy to Coolify** (or your server)
   - Domain: `api.shravani.group`
   - Port: `3000` or `5000`
   - Set environment variable: `CORS_ORIGINS=https://translate.shravani.group`

2. **Verify Backend:**
   ```bash
   curl https://api.shravani.group/
   # Should return API info JSON
   ```

### Step 2: Deploy Frontend

1. **Copy frontend files** to your web server:
   ```bash
   # Example: Copy to Nginx directory
   cp -r frontend/* /var/www/translate.shravani.group/
   ```

2. **Configure web server** (Nginx/Apache) to serve files

3. **Set up SSL** for `translate.shravani.group`

4. **Verify Frontend:**
   - Visit: `https://translate.shravani.group/`
   - Check browser console for API calls to `api.shravani.group`

### Step 3: Test Integration

1. **Open browser console** on frontend
2. **Check API calls:**
   - Should see requests to `https://api.shravani.group/...`
   - No CORS errors
3. **Test translation:**
   - Enter text and translate
   - Should work without errors

## Environment Variables

### Backend Server (`api.shravani.group`)

```bash
# Server
HOST=0.0.0.0
PORT=3000

# CORS (IMPORTANT!)
CORS_ORIGINS=https://translate.shravani.group

# API Security
API_KEY_REQUIRED=false  # Set to true if you want API key auth

# Translation
AUTO_INSTALL_MODELS=true
UPDATE_MODELS=false
```

### Frontend Server (`translate.shravani.group`)

No environment variables needed - it's just static files.

## CORS Configuration Details

The backend uses FastAPI's CORS middleware:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,  # Your frontend domain
    allow_credentials=True,  # Allows cookies/auth headers
    allow_methods=["*"],  # All HTTP methods
    allow_headers=["*"],  # All headers
)
```

**Important:** 
- Set `CORS_ORIGINS` to your exact frontend domain
- Include protocol (`https://`)
- No trailing slash
- For multiple origins, use comma-separated list

## Troubleshooting

### CORS Errors

**Error:** `Access to fetch at 'https://api.shravani.group/...' from origin 'https://translate.shravani.group' has been blocked by CORS policy`

**Solution:**
1. Check `CORS_ORIGINS` environment variable on backend
2. Ensure it includes: `https://translate.shravani.group`
3. Restart backend server
4. Check browser console for exact error

### API Not Found

**Error:** `404 Not Found` when calling API

**Solution:**
1. Verify backend is running at `api.shravani.group`
2. Check API URL in frontend JavaScript
3. Test API directly: `curl https://api.shravani.group/languages`

### Frontend Not Loading

**Error:** Blank page or 404

**Solution:**
1. Verify frontend files are in correct directory
2. Check web server configuration
3. Ensure `index.html` is in root of frontend directory
4. Check browser console for errors

## Development Setup

For local development with separate servers:

### Backend (Port 5000)
```bash
# Terminal 1
python main.py
# Backend runs on http://localhost:5000
```

### Frontend (Port 3000)
```bash
# Terminal 2
# Option 1: Simple HTTP server
cd frontend
python -m http.server 3000

# Option 2: Node.js
npx serve -s . -p 3000

# Option 3: Nginx (if installed)
# Configure nginx to serve frontend/ directory
```

### Update Frontend for Development

Edit `frontend/js/app.js`:

```javascript
const API_BASE_URL = 'http://localhost:5000';  // Local backend
```

## Production Checklist

- [ ] Backend deployed at `api.shravani.group`
- [ ] Frontend deployed at `translate.shravani.group`
- [ ] CORS configured: `CORS_ORIGINS=https://translate.shravani.group`
- [ ] SSL certificates installed for both domains
- [ ] Frontend JavaScript uses correct API URL
- [ ] Test translation works end-to-end
- [ ] Test authentication (signup/login)
- [ ] Test subscription upgrade
- [ ] Monitor CORS errors in browser console
- [ ] Check API logs for errors

## Benefits of Separate Servers

✅ **Scalability**: Scale frontend and backend independently  
✅ **Performance**: CDN for static files, optimized API server  
✅ **Security**: API server can have stricter firewall rules  
✅ **Flexibility**: Use different technologies for frontend/backend  
✅ **Deployment**: Deploy updates independently  

## Next Steps

1. Deploy backend to `api.shravani.group`
2. Deploy frontend to `translate.shravani.group`
3. Configure CORS on backend
4. Test integration
5. Monitor for errors

---

**Need Help?** Check the main [README.md](README.md) or [TECHNICAL_DOCUMENTATION.md](TECHNICAL_DOCUMENTATION.md)

