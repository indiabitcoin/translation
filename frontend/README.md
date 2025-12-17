# LibreTranslate Frontend

Modern, responsive web frontend for LibreTranslate translation service.

## Features

- 🚀 **Modern UI**: Clean, intuitive translation interface
- 🌍 **100+ Languages**: Support for world-class language coverage
- 👤 **User Authentication**: Sign up, login, and session management
- 💳 **Subscription Plans**: Free, Pro, and Enterprise plans
- 📊 **Usage Tracking**: Real-time usage statistics and limits
- 🔄 **Auto-translate**: Automatically translates as you type
- 🎯 **Language Detection**: Automatic source language detection
- 🔊 **Text-to-Speech**: Listen to translations
- 📋 **Copy to Clipboard**: One-click copy functionality

## Quick Start

### Option 1: Static File Hosting (Recommended)

Deploy the frontend files to any static file hosting service:

- **Nginx/Apache**: See `nginx.conf.example` or `apache.conf.example`
- **Cloudflare Pages**: Connect repository and deploy
- **Vercel**: Connect repository and deploy
- **Netlify**: Connect repository and deploy
- **GitHub Pages**: Enable Pages in repository settings

### Option 2: Node.js Server

```bash
npm install
npm start
```

Server runs on `http://localhost:3000` by default.

### Option 3: Simple HTTP Server

```bash
# Python
python -m http.server 3000

# Node.js
npx serve -s . -p 3000
```

## Configuration

### API Server URL

The frontend automatically detects the API server:

- **Production** (`translate.shravani.group`): Uses `https://api.shravani.group`
- **Development** (`localhost`): Uses same origin

To manually configure, edit `js/app.js`:

```javascript
const API_BASE_URL = 'https://api.shravani.group';  // Your API server
```

## Deployment

### Using Deployment Script

```bash
./deploy.sh nginx    # For Nginx
./deploy.sh apache   # For Apache
./deploy.sh node     # For Node.js
```

### Manual Deployment

1. **Copy files** to your web server directory
2. **Configure web server** (see `nginx.conf.example` or `apache.conf.example`)
3. **Set up SSL** certificate
4. **Update DNS** to point to your server

## File Structure

```
frontend/
├── index.html              # Main HTML file
├── css/
│   └── style.css          # All styles
├── js/
│   └── app.js             # Application logic
├── nginx.conf.example     # Nginx configuration
├── apache.conf.example    # Apache configuration
├── server.js              # Node.js Express server
├── package.json           # Node.js dependencies
├── deploy.sh              # Deployment script
└── README.md              # This file
```

## API Integration

The frontend communicates with the backend API at `https://api.shravani.group/`:

### Endpoints Used

- `POST /api/auth/signup` - User registration
- `POST /api/auth/login` - User authentication
- `GET /api/user/usage` - Get usage statistics
- `POST /api/subscription/upgrade` - Upgrade plan
- `POST /translate` - Translate text
- `POST /detect` - Detect language
- `GET /languages` - Get available languages

## Subscription Plans

### Free Plan
- 10,000 characters/month
- 50+ languages
- Basic translation

### Pro Plan ($9.99/month)
- 1,000,000 characters/month
- 100+ languages
- Priority support
- API access

### Enterprise Plan ($49.99/month)
- Unlimited characters
- 100+ languages
- 24/7 support
- Custom API limits

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Development

### Local Development

1. **Start backend API** (separate server):
   ```bash
   # On backend server
   python main.py
   ```

2. **Start frontend**:
   ```bash
   # Option 1: Node.js
   npm install
   npm start
   
   # Option 2: Simple server
   python -m http.server 3000
   ```

3. **Update API URL** in `js/app.js` for local development:
   ```javascript
   const API_BASE_URL = 'http://localhost:5000';  // Local backend
   ```

## Requirements

- Modern web browser with JavaScript enabled
- Backend API server running (see main repository)
- CORS configured on backend for frontend domain

## Security

- HTTPS required in production
- Security headers configured (X-Frame-Options, CSP, etc.)
- No sensitive data in client-side code
- API keys stored securely

## Troubleshooting

### CORS Errors

Ensure backend has `CORS_ORIGINS` set to your frontend domain:
```
CORS_ORIGINS=https://translate.shravani.group
```

### API Not Found

1. Verify backend is running at API URL
2. Check API URL in `js/app.js`
3. Test API directly: `curl https://api.shravani.group/languages`

### Frontend Not Loading

1. Check file permissions
2. Verify web server configuration
3. Check browser console for errors

## Related Repositories

- **Backend API**: [translation](https://github.com/indiabitcoin/translation) - Main repository with backend API

## License

MIT License

## Support

For issues or questions:
1. Check the main [README](../README.md) in backend repository
2. Review [SEPARATE_SERVERS_SETUP.md](../SEPARATE_SERVERS_SETUP.md)
3. Check [DEPLOYMENT_CHECKLIST.md](../DEPLOYMENT_CHECKLIST.md)

---

**Live Demo**: https://translate.shravani.group/  
**API Server**: https://api.shravani.group/

