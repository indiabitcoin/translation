# Quick Security Setup Guide

## 🔒 Enable API Key Authentication in 3 Steps

### Step 1: Generate API Keys

Run the key generator:
```bash
python generate_api_key.py
```

Or generate manually:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

**Example output:**
```
API Key 1: a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6
```

### Step 2: Configure in Coolify

1. Go to your Coolify dashboard
2. Select your translation server application
3. Go to **Environment Variables**
4. Add these variables:

```
API_KEY_REQUIRED=true
API_KEYS=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6
```

**For multiple keys (comma-separated):**
```
API_KEYS=key1,key2,key3
```

5. Click **Save** and **Restart** your application

### Step 3: Update Your Code

**JavaScript:**
```javascript
const response = await fetch('https://translate.shravani.group/translate', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-API-Key': 'a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6'
  },
  body: JSON.stringify({
    q: "Hello",
    source: "en",
    target: "es"
  })
});
```

**Using the TranslationClient:**
```javascript
const client = new TranslationClient(
  'https://translate.shravani.group/',
  'a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6'
);
const translated = await client.translate("Hello", "en", "es");
```

## ✅ Test It Works

**Test without key (should fail):**
```bash
curl -X POST https://translate.shravani.group/translate \
  -H "Content-Type: application/json" \
  -d '{"q": "Hello", "source": "en", "target": "es"}'
```

Expected: `{"detail": "API key required"}`

**Test with key (should work):**
```bash
curl -X POST https://translate.shravani.group/translate \
  -H "Content-Type: application/json" \
  -H "X-API-Key: a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6" \
  -d '{"q": "Hello", "source": "en", "target": "es"}'
```

Expected: `{"translatedText": "Hola"}`

## 🔐 Additional Security: Restrict CORS

Limit which domains can access your API:

```
CORS_ORIGINS=https://yourwebsite.com,https://app.example.com
```

## 📚 More Information

- Full guide: [SECURITY.md](../SECURITY.md)
- Integration examples: [INTEGRATION_GUIDE.md](../INTEGRATION_GUIDE.md)
- Coolify deployment: [COOLIFY_DEPLOYMENT.md](../COOLIFY_DEPLOYMENT.md)

