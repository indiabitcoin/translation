# Frontend Documentation

## Overview

The LibreTranslate frontend is a modern, responsive web application that provides a user-friendly interface for translation services with subscription plan management.

## Features

### 🎯 Core Features
- **Translation Interface**: Clean, intuitive translation UI with source and target language selection
- **Auto-translation**: Automatically translates as you type (with debouncing)
- **Language Detection**: Automatic language detection for source text
- **Text-to-Speech**: Listen to translations using browser's speech synthesis
- **Copy to Clipboard**: One-click copy of translated text
- **Language Swap**: Quickly swap source and target languages

### 👤 User Management
- **User Authentication**: Sign up and sign in with email/password
- **Session Management**: Persistent login using JWT tokens
- **User Dashboard**: View usage statistics and plan information

### 💳 Subscription Plans
- **Free Plan**: 10,000 characters/month
  - 50+ languages
  - Basic translation
  - Language detection
  
- **Pro Plan**: $9.99/month - 1,000,000 characters/month
  - 100+ languages
  - Advanced translation
  - Priority support
  - API access
  
- **Enterprise Plan**: $49.99/month - Unlimited characters
  - 100+ languages
  - Advanced translation
  - 24/7 support
  - Custom API limits

### 📊 Usage Tracking
- Real-time usage display
- Progress bars showing character usage
- Automatic monthly reset
- Usage limit enforcement

## File Structure

```
frontend/
├── index.html          # Main HTML file
├── css/
│   └── style.css      # All styles
└── js/
    └── app.js          # Application logic
```

## API Integration

The frontend communicates with the backend through the following endpoints:

### Authentication
- `POST /api/auth/signup` - Create new account
- `POST /api/auth/login` - Authenticate user
- `GET /api/user/usage` - Get usage statistics
- `POST /api/user/usage` - Update usage (internal)

### Translation
- `POST /translate` - Translate text
- `POST /detect` - Detect language
- `GET /languages` - Get available languages

### Subscription
- `POST /api/subscription/upgrade` - Upgrade plan

## Usage

### Development

1. **Start the backend server:**
   ```bash
   python main.py
   ```

2. **Access the frontend:**
   Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

### Production

The frontend is automatically served by FastAPI when the server starts. No additional build step is required.

## Configuration

### API URL

The frontend automatically detects the API URL from the current window location. To use a different API server, modify `AppState.apiUrl` in `frontend/js/app.js`:

```javascript
const AppState = {
    apiUrl: 'https://your-api-server.com'
};
```

## User Storage

User data is stored in `users.json` in the project root. This file contains:
- User credentials (hashed passwords)
- API keys
- Subscription plans
- Usage statistics

**⚠️ Security Note**: In production, use a proper database (PostgreSQL, MongoDB, etc.) instead of JSON file storage.

## Authentication Flow

1. User signs up or logs in
2. Backend returns JWT token
3. Token stored in `localStorage`
4. Token sent with API requests via `Authorization` header
5. Backend validates token and returns user data

## Subscription Flow

1. User clicks "Upgrade" button
2. Frontend sends upgrade request with plan name
3. Backend updates user plan in database
4. Frontend updates UI with new plan limits
5. Usage limits are enforced on translation requests

## Usage Tracking

- Usage is tracked per character translated
- Limits reset monthly (30 days from signup/upgrade)
- Usage is checked before each translation
- Users are redirected to pricing page if limit exceeded

## Browser Compatibility

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Customization

### Styling

Modify `frontend/css/style.css` to customize:
- Colors (CSS variables in `:root`)
- Layout and spacing
- Typography
- Component styles

### Functionality

Modify `frontend/js/app.js` to customize:
- API endpoints
- User interface behavior
- Feature flags
- Default settings

## Troubleshooting

### Frontend not loading
- Check that `frontend/` directory exists
- Verify static file serving is configured in `main.py`
- Check browser console for errors

### Authentication not working
- Verify JWT_SECRET_KEY is set in environment
- Check that `users.json` is writable
- Review backend logs for errors

### Translation failing
- Check API key is valid
- Verify usage limits haven't been exceeded
- Check network tab for API errors

## Security Considerations

1. **Password Storage**: Passwords are hashed using SHA-256 (consider bcrypt for production)
2. **JWT Tokens**: Tokens expire after 30 days
3. **API Keys**: Each user gets a unique API key
4. **CORS**: Configure CORS origins in backend settings
5. **HTTPS**: Always use HTTPS in production

## Future Enhancements

- [ ] Payment integration (Stripe, PayPal)
- [ ] Email verification
- [ ] Password reset functionality
- [ ] Two-factor authentication
- [ ] Usage analytics dashboard
- [ ] Batch translation
- [ ] File translation (PDF, DOCX)
- [ ] Translation history
- [ ] Favorite translations
- [ ] Dark mode
- [ ] Multi-language UI

## Support

For issues or questions:
1. Check the main [README.md](../README.md)
2. Review [API_REFERENCE.md](../API_REFERENCE.md)
3. Check backend logs for errors
4. Open an issue on GitHub

