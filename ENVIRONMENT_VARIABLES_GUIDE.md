# Using Environment Variables for API Keys in Your Websites

**✅ Best Practice:** Never hardcode API keys in your code! Use environment variables instead.

## 📋 Platform-Specific Guides

### 1. Next.js (React Framework)

**Step 1: Create `.env.local` file** (in your Next.js project root)
```bash
# .env.local (never commit this file!)
NEXT_PUBLIC_TRANSLATE_API_KEY=your-api-key-here
```

**Step 2: Use in your code**
```javascript
// pages/api/translate.js or components/TranslateButton.jsx
const apiKey = process.env.NEXT_PUBLIC_TRANSLATE_API_KEY;

async function translate(text, source, target) {
  const response = await fetch('https://translate.shravani.group/translate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-API-Key': apiKey  // ← From environment variable
    },
    body: JSON.stringify({ q: text, source, target })
  });
  return response.json();
}
```

**Step 3: Add to `.gitignore`**
```bash
# .gitignore
.env.local
.env*.local
```

**Step 4: For Production (Vercel/Netlify/etc.)**
- Go to your hosting platform's dashboard
- Navigate to **Environment Variables** settings
- Add: `NEXT_PUBLIC_TRANSLATE_API_KEY` = `your-api-key-here`
- Redeploy your application

---

### 2. React (Create React App)

**Step 1: Create `.env` file** (in your React project root)
```bash
# .env (never commit this file!)
REACT_APP_TRANSLATE_API_KEY=your-api-key-here
```

**Important:** Variable names must start with `REACT_APP_` to be accessible in React!

**Step 2: Use in your code**
```javascript
// src/services/translation.js
const apiKey = process.env.REACT_APP_TRANSLATE_API_KEY;

export async function translate(text, source, target) {
  const response = await fetch('https://translate.shravani.group/translate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-API-Key': apiKey
    },
    body: JSON.stringify({ q: text, source, target })
  });
  return response.json();
}
```

**Step 3: Add to `.gitignore`**
```bash
# .gitignore
.env
.env.local
.env.development.local
.env.test.local
.env.production.local
```

**Step 4: For Production**
- **Netlify:** Site Settings → Environment Variables
- **Vercel:** Project Settings → Environment Variables
- **Other platforms:** Check their documentation for environment variable settings

---

### 3. Vue.js

**Step 1: Create `.env` file**
```bash
# .env (never commit!)
VUE_APP_TRANSLATE_API_KEY=your-api-key-here
```

**Important:** Variable names must start with `VUE_APP_` to be accessible!

**Step 2: Use in your code**
```javascript
// src/services/translation.js
const apiKey = process.env.VUE_APP_TRANSLATE_API_KEY;

export async function translate(text, source, target) {
  const response = await fetch('https://translate.shravani.group/translate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-API-Key': apiKey
    },
    body: JSON.stringify({ q: text, source, target })
  });
  return response.json();
}
```

**Step 3: Add to `.gitignore`**
```bash
.env
.env.local
.env.*.local
```

---

### 4. Plain HTML/JavaScript (Static Sites)

**Option A: Using a Build Tool (Vite/Webpack)**

Create `.env` file:
```bash
VITE_TRANSLATE_API_KEY=your-api-key-here
```

Use in code:
```javascript
const apiKey = import.meta.env.VITE_TRANSLATE_API_KEY;
```

**Option B: Server-Side Proxy (Recommended for Static Sites)**

Since environment variables aren't available in plain HTML/JS, use a server-side proxy:

**Backend Proxy (Node.js/Express):**
```javascript
// server.js (runs on your server)
require('dotenv').config();
const express = require('express');
const app = express();

app.post('/api/translate', async (req, res) => {
  const response = await fetch('https://translate.shravani.group/translate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-API-Key': process.env.TRANSLATE_API_KEY  // ← Server-side only
    },
    body: JSON.stringify(req.body)
  });
  const data = await response.json();
  res.json(data);
});

app.listen(3000);
```

**Frontend (Plain HTML/JS):**
```javascript
// No API key needed here - proxy handles it
fetch('/api/translate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ q: "Hello", source: "en", target: "es" })
});
```

---

### 5. WordPress

**Option A: Using wp-config.php**
```php
// wp-config.php
define('TRANSLATE_API_KEY', 'your-api-key-here');
```

**Option B: Using WordPress Environment Variables Plugin**
- Install a plugin like "WP Environment Variables"
- Add: `TRANSLATE_API_KEY` = `your-api-key-here`

**Use in PHP:**
```php
$apiKey = getenv('TRANSLATE_API_KEY') ?: TRANSLATE_API_KEY;

$response = wp_remote_post('https://translate.shravani.group/translate', [
    'headers' => [
        'Content-Type' => 'application/json',
        'X-API-Key' => $apiKey
    ],
    'body' => json_encode([
        'q' => 'Hello',
        'source' => 'en',
        'target' => 'es'
    ])
]);
```

---

### 6. Node.js (Backend/Server)

**Step 1: Install dotenv**
```bash
npm install dotenv
```

**Step 2: Create `.env` file**
```bash
# .env
TRANSLATE_API_KEY=your-api-key-here
```

**Step 3: Load in your code**
```javascript
// server.js
require('dotenv').config();

const apiKey = process.env.TRANSLATE_API_KEY;

async function translate(text, source, target) {
  const response = await fetch('https://translate.shravani.group/translate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-API-Key': apiKey
    },
    body: JSON.stringify({ q: text, source, target })
  });
  return response.json();
}
```

**Step 4: Add to `.gitignore`**
```bash
.env
.env.local
```

---

### 7. Using TranslationClient with Environment Variables

**Update your code to use environment variables:**

```javascript
// Instead of hardcoding:
// const client = new TranslationClient('https://translate.shravani.group/', 'hardcoded-key');

// Use environment variable:
const apiKey = process.env.REACT_APP_TRANSLATE_API_KEY || 
               process.env.NEXT_PUBLIC_TRANSLATE_API_KEY || 
               process.env.VUE_APP_TRANSLATE_API_KEY;

const client = new TranslationClient(
  'https://translate.shravani.group/',
  apiKey  // ← From environment variable
);

// Now use it
const translated = await client.translate("Hello", "en", "es");
```

---

## 🔐 Security Checklist

- ✅ **Never commit `.env` files to Git**
- ✅ **Add `.env*` to `.gitignore`**
- ✅ **Use different keys for development and production**
- ✅ **Rotate keys periodically**
- ✅ **Store production keys in your hosting platform's environment variables**

---

## 📝 Example `.gitignore` Entry

```bash
# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local
.env*.local
```

---

## 🚀 Deployment Platforms

### Vercel
1. Go to Project Settings → Environment Variables
2. Add: `NEXT_PUBLIC_TRANSLATE_API_KEY` = `your-key`
3. Redeploy

### Netlify
1. Go to Site Settings → Environment Variables
2. Add: `REACT_APP_TRANSLATE_API_KEY` = `your-key`
3. Redeploy

### Heroku
```bash
heroku config:set TRANSLATE_API_KEY=your-key
```

### Railway
1. Go to Project → Variables
2. Add: `TRANSLATE_API_KEY` = `your-key`
3. Redeploy

### Coolify (for your websites)
1. Go to your website application
2. Environment Variables
3. Add: `REACT_APP_TRANSLATE_API_KEY` = `your-key`
4. Redeploy

---

## 🎯 Quick Reference

| Platform | Env File | Variable Prefix | Example |
|----------|----------|-----------------|---------|
| Next.js | `.env.local` | `NEXT_PUBLIC_` | `NEXT_PUBLIC_TRANSLATE_API_KEY` |
| React (CRA) | `.env` | `REACT_APP_` | `REACT_APP_TRANSLATE_API_KEY` |
| Vue.js | `.env` | `VUE_APP_` | `VUE_APP_TRANSLATE_API_KEY` |
| Vite | `.env` | `VITE_` | `VITE_TRANSLATE_API_KEY` |
| Node.js | `.env` | None | `TRANSLATE_API_KEY` |
| WordPress | `wp-config.php` | None | `TRANSLATE_API_KEY` |

---

## 📚 More Examples

See `examples/translation-client.js` for a complete client implementation that supports API keys from environment variables.

