# API Key Configuration: Where to Set Them Up

## 🔑 Two Places, Two Different Roles

### 1. **Translation Server** (Backend - https://translate.shravani.group/)
**Purpose:** Define which API keys are valid

**What to do:**
- Configure environment variables in **Coolify** (or your server)
- This tells the server: "Only accept these API keys"

**Configuration:**
```
API_KEY_REQUIRED=true
API_KEYS=key1,key2,key3
```

**Location:** Coolify Dashboard → Your Translation Server → Environment Variables

---

### 2. **End Server/Website** (Client - Your web apps)
**Purpose:** Use the API key when making requests

**What to do:**
- Include the API key in your code when calling the translation API
- This tells the server: "I'm authorized to use this service"

**Usage Example:**
```javascript
// In your website's JavaScript code
fetch('https://translate.shravani.group/translate', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-API-Key': 'key1'  // ← Use one of the keys you configured on the server
  },
  body: JSON.stringify({...})
});
```

---

## 📋 Step-by-Step Setup

### Step 1: Configure on Translation Server (Coolify)

1. **Generate API keys:**
   ```bash
   python generate_api_key.py
   ```
   Output: `API_KEYS=abc123xyz,def456uvw`

2. **Go to Coolify:**
   - Open your translation server application
   - Navigate to **Environment Variables**
   - Add:
     ```
     API_KEY_REQUIRED=true
     API_KEYS=abc123xyz,def456uvw
     ```
   - **Save** and **Restart** the server

3. **Verify it's working:**
   ```bash
   # Without key (should fail)
   curl -X POST https://translate.shravani.group/translate \
     -H "Content-Type: application/json" \
     -d '{"q": "Hello", "source": "en", "target": "es"}'
   # Returns: {"detail": "API key required"}
   
   # With key (should work)
   curl -X POST https://translate.shravani.group/translate \
     -H "Content-Type: application/json" \
     -H "X-API-Key: abc123xyz" \
     -d '{"q": "Hello", "source": "en", "target": "es"}'
   # Returns: {"translatedText": "Hola"}
   ```

### Step 2: Use on Your Websites/Web Apps

**✅ RECOMMENDED: Store in Environment Variables (Never Hardcode!)**

**For Next.js:**
```javascript
// .env.local (never commit this file!)
NEXT_PUBLIC_TRANSLATE_API_KEY=abc123xyz

// In your code
const apiKey = process.env.NEXT_PUBLIC_TRANSLATE_API_KEY;

fetch('https://translate.shravani.group/translate', {
  headers: {
    'X-API-Key': apiKey  // ← From environment variable
  },
  // ...
});
```

**For React (Create React App):**
```javascript
// .env (never commit!)
REACT_APP_TRANSLATE_API_KEY=abc123xyz

// In your code
const apiKey = process.env.REACT_APP_TRANSLATE_API_KEY;
```

**For Vue.js:**
```javascript
// .env (never commit!)
VUE_APP_TRANSLATE_API_KEY=abc123xyz

// In your code
const apiKey = process.env.VUE_APP_TRANSLATE_API_KEY;
```

**For Node.js/Express:**
```javascript
// .env (never commit!)
TRANSLATE_API_KEY=abc123xyz

// In your code
require('dotenv').config();
const apiKey = process.env.TRANSLATE_API_KEY;
```

**📚 See [ENVIRONMENT_VARIABLES_GUIDE.md](ENVIRONMENT_VARIABLES_GUIDE.md) for detailed platform-specific instructions!**

**Option B: Use Different Keys for Different Apps**

On translation server, configure multiple keys:
```
API_KEYS=key-for-website1,key-for-website2,key-for-mobile-app
```

Then use different keys in different apps:
- Website 1 uses: `key-for-website1`
- Website 2 uses: `key-for-website2`
- Mobile app uses: `key-for-mobile-app`

This way you can revoke access per application!

---

## 🎯 Real-World Example

### Scenario: You have 3 websites that need translation

**1. Configure on Translation Server (Coolify):**
```
API_KEY_REQUIRED=true
API_KEYS=website1-key-abc123,website2-key-def456,website3-key-ghi789
```

**2. Use on Website 1:**
```javascript
// website1.com code
const client = new TranslationClient(
  'https://translate.shravani.group/',
  'website1-key-abc123'  // ← Key for this website
);
```

**3. Use on Website 2:**
```javascript
// website2.com code
const client = new TranslationClient(
  'https://translate.shravani.group/',
  'website2-key-def456'  // ← Different key for this website
);
```

**4. Use on Website 3:**
```javascript
// website3.com code
const client = new TranslationClient(
  'https://translate.shravani.group/',
  'website3-key-ghi789'  // ← Different key for this website
);
```

---

## 🔐 Security Best Practices

### ✅ DO:
- ✅ Configure API keys on **translation server** (Coolify)
- ✅ Store API keys in **environment variables** on your websites (never hardcode)
- ✅ Use different keys for different applications
- ✅ Keep keys secret (never commit to Git)
- ✅ Rotate keys periodically

### ❌ DON'T:
- ❌ Hardcode API keys in your website's JavaScript (visible to anyone)
- ❌ Commit API keys to Git repositories
- ❌ Share the same key across all applications
- ❌ Use weak or predictable keys

---

## 📍 Summary

| Location | What to Do | Purpose |
|----------|------------|---------|
| **Translation Server** (Coolify) | Configure `API_KEY_REQUIRED=true` and `API_KEYS=...` | Define valid keys |
| **Your Websites/Apps** | Include `X-API-Key` header in requests | Authenticate requests |

**Think of it like a door lock:**
- **Translation Server** = The lock (defines which keys work)
- **Your Websites** = The keys (use them to unlock access)

Both are needed for security to work!

