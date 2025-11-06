# Security Guide: Protecting Your Translation API

Your translation server is currently **publicly accessible** without authentication. This guide shows you how to secure it.

## 🔒 Enable API Key Authentication

### Step 1: Generate Secure API Keys

Generate strong, random API keys. Here are a few methods:

**Using Python:**
```python
import secrets
api_key = secrets.token_urlsafe(32)
print(api_key)
```

**Using OpenSSL:**
```bash
openssl rand -hex 32
```

**Using Node.js:**
```javascript
const crypto = require('crypto');
const apiKey = crypto.randomBytes(32).toString('hex');
console.log(apiKey);
```

**Online Generator:**
- Use a secure password generator
- Generate at least 32 characters
- Use alphanumeric characters

### Step 2: Configure Environment Variables

#### For Coolify Deployment:

1. Go to your Coolify project dashboard
2. Navigate to your translation server application
3. Go to **Environment Variables** section
4. Add these variables:

```
API_KEY_REQUIRED=true
API_KEYS=your-secret-key-1,your-secret-key-2,another-key
```

**Example:**
```
API_KEY_REQUIRED=true
API_KEYS=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6,another-secure-key-here
```

5. **Restart** your application after adding the variables

#### For Docker Compose (Local):

Edit your `docker-compose.yml`:
```yaml
services:
  libretranslate:
    environment:
      - API_KEY_REQUIRED=true
      - API_KEYS=your-secret-key-1,your-secret-key-2
```

#### For Direct Python Run:

Create/update `.env` file:
```bash
API_KEY_REQUIRED=true
API_KEYS=your-secret-key-1,your-secret-key-2
```

### Step 3: Test the Security

**Without API Key (should fail):**
```bash
curl -X POST https://translate.shravani.group/translate \
  -H "Content-Type: application/json" \
  -d '{"q": "Hello", "source": "en", "target": "es"}'
```

Expected response:
```json
{"detail": "API key required"}
```

**With API Key (should work):**
```bash
curl -X POST https://translate.shravani.group/translate \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-secret-key-1" \
  -d '{"q": "Hello", "source": "en", "target": "es"}'
```

Expected response:
```json
{"translatedText": "Hola"}
```

## 🔐 Multiple API Keys

You can configure multiple API keys by separating them with commas:

```
API_KEYS=key-for-app1,key-for-app2,key-for-website,admin-key
```

This allows you to:
- Use different keys for different applications
- Revoke access by removing a key
- Track usage per application (if you add logging)

## 🌐 CORS Configuration (Additional Security)

Restrict which domains can access your API:

```
CORS_ORIGINS=https://yourwebsite.com,https://app.example.com
```

**For multiple domains:**
```
CORS_ORIGINS=https://site1.com,https://site2.com,https://localhost:3000
```

**Allow all (development only):**
```
CORS_ORIGINS=*
```

## 📝 Using API Keys in Your Applications

### JavaScript/Fetch
```javascript
const response = await fetch('https://translate.shravani.group/translate', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-API-Key': 'your-secret-key-1'  // Add this header
  },
  body: JSON.stringify({
    q: "Hello, world!",
    source: "en",
    target: "es"
  })
});
```

### cURL
```bash
curl -X POST https://translate.shravani.group/translate \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-secret-key-1" \
  -d '{"q": "Hello", "source": "en", "target": "es"}'
```

### Python
```python
import requests

headers = {
    'Content-Type': 'application/json',
    'X-API-Key': 'your-secret-key-1'
}

data = {
    'q': 'Hello, world!',
    'source': 'en',
    'target': 'es'
}

response = requests.post(
    'https://translate.shravani.group/translate',
    headers=headers,
    json=data
)
print(response.json())
```

### React/Next.js
```javascript
// Store API key in environment variable (never commit to git!)
const API_KEY = process.env.NEXT_PUBLIC_TRANSLATE_API_KEY;

async function translate(text, source, target) {
  const response = await fetch('https://translate.shravani.group/translate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-API-Key': API_KEY
    },
    body: JSON.stringify({ q: text, source, target })
  });
  return response.json();
}
```

## 🛡️ Security Best Practices

1. **Never commit API keys to Git**
   - Use environment variables
   - Add `.env` to `.gitignore`
   - Use secrets management in production

2. **Use HTTPS**
   - Your server should use HTTPS (which it does: https://translate.shravani.group/)
   - This encrypts API keys in transit

3. **Rotate API Keys Regularly**
   - Change keys periodically
   - Immediately revoke compromised keys

4. **Limit CORS Origins**
   - Don't use `CORS_ORIGINS=*` in production
   - Specify exact domains that need access

5. **Monitor Usage**
   - Consider adding rate limiting
   - Log API key usage for monitoring
   - Set up alerts for unusual activity

6. **Use Different Keys for Different Apps**
   - Easier to revoke access per application
   - Better tracking and monitoring

## 🚨 Quick Enable Checklist

- [ ] Generate secure API keys (32+ characters)
- [ ] Add `API_KEY_REQUIRED=true` to environment variables
- [ ] Add `API_KEYS=key1,key2,...` to environment variables
- [ ] Restart your server
- [ ] Test without API key (should fail)
- [ ] Test with API key (should work)
- [ ] Update your applications to include API key header
- [ ] Restrict CORS origins if needed
- [ ] Document your API keys securely (password manager)

## 🔄 Disabling API Key Authentication

If you need to disable authentication temporarily:

```
API_KEY_REQUIRED=false
```

Or remove the environment variable entirely (defaults to `false`).

## 📚 Additional Resources

- See `INTEGRATION_GUIDE.md` for more code examples
- See `COOLIFY_DEPLOYMENT.md` for deployment-specific instructions
- See `examples/` directory for ready-to-use code snippets

