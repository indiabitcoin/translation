# Integration Guide: Using Translation API in Your Web Apps

This guide shows how to integrate the LibreTranslate server with different web applications and websites.

## Table of Contents

1. [Quick Start](#quick-start)
2. [JavaScript/Browser Integration](#javascriptbrowser-integration)
3. [React Integration](#react-integration)
4. [Vue.js Integration](#vuejs-integration)
5. [Python Backend Integration](#python-backend-integration)
6. [Node.js Integration](#nodejs-integration)
7. [PHP Integration](#php-integration)
8. [CORS Configuration](#cors-configuration)
9. [API Authentication](#api-authentication)
10. [Error Handling](#error-handling)
11. [Best Practices](#best-practices)

## Quick Start

**Base URL:** `http://your-server.com:5000` (or your deployed URL)

**Main Endpoints:**
- `POST /translate` - Translate text
- `GET /languages` - Get supported languages
- `POST /detect` - Detect language
- `GET /health` - Health check

## JavaScript/Browser Integration

### Vanilla JavaScript

```javascript
// Translation function
async function translateText(text, sourceLang, targetLang) {
  const response = await fetch('http://your-server.com:5000/translate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      q: text,
      source: sourceLang,
      target: targetLang,
      format: 'text'
    })
  });
  
  if (!response.ok) {
    throw new Error(`Translation failed: ${response.statusText}`);
  }
  
  const data = await response.json();
  return data.translatedText;
}

// Usage example
translateText('Hello, world!', 'en', 'es')
  .then(translated => console.log(translated)) // "¡Hola, mundo!"
  .catch(error => console.error('Error:', error));
```

### With Error Handling and Retry

```javascript
async function translateText(text, sourceLang, targetLang, retries = 3) {
  for (let i = 0; i < retries; i++) {
    try {
      const response = await fetch('http://your-server.com:5000/translate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          q: text,
          source: sourceLang,
          target: targetLang,
          format: 'text'
        })
      });
      
      if (!response.ok) {
        if (response.status === 503) {
          // Service unavailable, wait and retry
          await new Promise(resolve => setTimeout(resolve, 1000 * (i + 1)));
          continue;
        }
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      const data = await response.json();
      return data.translatedText;
    } catch (error) {
      if (i === retries - 1) throw error;
      await new Promise(resolve => setTimeout(resolve, 1000 * (i + 1)));
    }
  }
}
```

### Get Available Languages

```javascript
async function getLanguages() {
  const response = await fetch('http://your-server.com:5000/languages');
  const languages = await response.json();
  return languages;
}

// Usage
getLanguages().then(langs => {
  console.log('Available languages:', langs);
  // [{code: "en", name: "English"}, {code: "es", name: "Spanish"}, ...]
});
```

### Language Detection

```javascript
async function detectLanguage(text) {
  const response = await fetch('http://your-server.com:5000/detect', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ q: text })
  });
  
  const data = await response.json();
  return data; // {language: "en", confidence: 0.95}
}
```

### Complete Translation Widget Example

```html
<!DOCTYPE html>
<html>
<head>
  <title>Translation Widget</title>
  <style>
    .translator {
      max-width: 600px;
      margin: 50px auto;
      padding: 20px;
      border: 1px solid #ddd;
      border-radius: 8px;
    }
    textarea {
      width: 100%;
      min-height: 100px;
      margin: 10px 0;
      padding: 10px;
    }
    select, button {
      padding: 10px;
      margin: 5px;
    }
    button {
      background: #007bff;
      color: white;
      border: none;
      cursor: pointer;
    }
    button:hover {
      background: #0056b3;
    }
  </style>
</head>
<body>
  <div class="translator">
    <h2>Translate Text</h2>
    
    <select id="sourceLang">
      <option value="auto">Auto-detect</option>
      <option value="en">English</option>
      <option value="es">Spanish</option>
      <option value="fr">French</option>
    </select>
    
    <select id="targetLang">
      <option value="es">Spanish</option>
      <option value="en">English</option>
      <option value="fr">French</option>
    </select>
    
    <textarea id="sourceText" placeholder="Enter text to translate..."></textarea>
    <button onclick="translate()">Translate</button>
    <textarea id="translatedText" placeholder="Translation will appear here..." readonly></textarea>
    
    <div id="error" style="color: red; display: none;"></div>
  </div>

  <script>
    const API_URL = 'http://your-server.com:5000'; // Change to your server URL
    
    async function translate() {
      const sourceText = document.getElementById('sourceText').value;
      const sourceLang = document.getElementById('sourceLang').value;
      const targetLang = document.getElementById('targetLang').value;
      const errorDiv = document.getElementById('error');
      const translatedText = document.getElementById('translatedText');
      
      if (!sourceText.trim()) {
        errorDiv.textContent = 'Please enter text to translate';
        errorDiv.style.display = 'block';
        return;
      }
      
      errorDiv.style.display = 'none';
      translatedText.value = 'Translating...';
      
      try {
        const response = await fetch(`${API_URL}/translate`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            q: sourceText,
            source: sourceLang,
            target: targetLang,
            format: 'text'
          })
        });
        
        if (!response.ok) {
          throw new Error(`Translation failed: ${response.statusText}`);
        }
        
        const data = await response.json();
        translatedText.value = data.translatedText;
      } catch (error) {
        errorDiv.textContent = `Error: ${error.message}`;
        errorDiv.style.display = 'block';
        translatedText.value = '';
      }
    }
  </script>
</body>
</html>
```

## React Integration

### React Component Example

```jsx
import React, { useState, useEffect } from 'react';

const API_URL = 'http://your-server.com:5000';

function Translator() {
  const [sourceText, setSourceText] = useState('');
  const [translatedText, setTranslatedText] = useState('');
  const [sourceLang, setSourceLang] = useState('en');
  const [targetLang, setTargetLang] = useState('es');
  const [languages, setLanguages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Load available languages on mount
  useEffect(() => {
    fetch(`${API_URL}/languages`)
      .then(res => res.json())
      .then(data => setLanguages(data))
      .catch(err => console.error('Failed to load languages:', err));
  }, []);

  const translate = async () => {
    if (!sourceText.trim()) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch(`${API_URL}/translate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          q: sourceText,
          source: sourceLang,
          target: targetLang,
          format: 'text'
        })
      });
      
      if (!response.ok) {
        throw new Error(`Translation failed: ${response.statusText}`);
      }
      
      const data = await response.json();
      setTranslatedText(data.translatedText);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="translator">
      <h2>Translate Text</h2>
      
      <select value={sourceLang} onChange={(e) => setSourceLang(e.target.value)}>
        <option value="auto">Auto-detect</option>
        {languages.map(lang => (
          <option key={lang.code} value={lang.code}>{lang.name}</option>
        ))}
      </select>
      
      <select value={targetLang} onChange={(e) => setTargetLang(e.target.value)}>
        {languages.map(lang => (
          <option key={lang.code} value={lang.code}>{lang.name}</option>
        ))}
      </select>
      
      <textarea
        value={sourceText}
        onChange={(e) => setSourceText(e.target.value)}
        placeholder="Enter text to translate..."
        rows={5}
      />
      
      <button onClick={translate} disabled={loading}>
        {loading ? 'Translating...' : 'Translate'}
      </button>
      
      <textarea
        value={translatedText}
        placeholder="Translation will appear here..."
        rows={5}
        readOnly
      />
      
      {error && <div className="error">{error}</div>}
    </div>
  );
}

export default Translator;
```

### Custom React Hook

```jsx
import { useState, useCallback } from 'react';

const API_URL = 'http://your-server.com:5000';

export function useTranslation() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const translate = useCallback(async (text, sourceLang, targetLang) => {
    if (!text.trim()) return null;
    
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch(`${API_URL}/translate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          q: text,
          source: sourceLang,
          target: targetLang,
          format: 'text'
        })
      });
      
      if (!response.ok) {
        throw new Error(`Translation failed: ${response.statusText}`);
      }
      
      const data = await response.json();
      return data.translatedText;
    } catch (err) {
      setError(err.message);
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  return { translate, loading, error };
}

// Usage in component:
function MyComponent() {
  const { translate, loading, error } = useTranslation();
  
  const handleTranslate = async () => {
    const result = await translate('Hello', 'en', 'es');
    console.log(result); // "Hola"
  };
  
  return <button onClick={handleTranslate}>Translate</button>;
}
```

## Vue.js Integration

```vue
<template>
  <div class="translator">
    <h2>Translate Text</h2>
    
    <select v-model="sourceLang">
      <option value="auto">Auto-detect</option>
      <option v-for="lang in languages" :key="lang.code" :value="lang.code">
        {{ lang.name }}
      </option>
    </select>
    
    <select v-model="targetLang">
      <option v-for="lang in languages" :key="lang.code" :value="lang.code">
        {{ lang.name }}
      </option>
    </select>
    
    <textarea v-model="sourceText" placeholder="Enter text to translate..."></textarea>
    <button @click="translate" :disabled="loading">
      {{ loading ? 'Translating...' : 'Translate' }}
    </button>
    <textarea v-model="translatedText" placeholder="Translation..." readonly></textarea>
    
    <div v-if="error" class="error">{{ error }}</div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      API_URL: 'http://your-server.com:5000',
      sourceText: '',
      translatedText: '',
      sourceLang: 'en',
      targetLang: 'es',
      languages: [],
      loading: false,
      error: null
    };
  },
  mounted() {
    this.loadLanguages();
  },
  methods: {
    async loadLanguages() {
      try {
        const response = await fetch(`${this.API_URL}/languages`);
        this.languages = await response.json();
      } catch (err) {
        console.error('Failed to load languages:', err);
      }
    },
    async translate() {
      if (!this.sourceText.trim()) return;
      
      this.loading = true;
      this.error = null;
      
      try {
        const response = await fetch(`${this.API_URL}/translate`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            q: this.sourceText,
            source: this.sourceLang,
            target: this.targetLang,
            format: 'text'
          })
        });
        
        if (!response.ok) {
          throw new Error(`Translation failed: ${response.statusText}`);
        }
        
        const data = await response.json();
        this.translatedText = data.translatedText;
      } catch (err) {
        this.error = err.message;
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>
```

## Python Backend Integration

### Using requests library

```python
import requests

class TranslationClient:
    def __init__(self, base_url='http://your-server.com:5000', api_key=None):
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {'Content-Type': 'application/json'}
        if api_key:
            self.headers['X-API-Key'] = api_key
    
    def translate(self, text, source='auto', target='en', format_type='text'):
        """Translate text from source to target language."""
        response = requests.post(
            f'{self.base_url}/translate',
            json={
                'q': text,
                'source': source,
                'target': target,
                'format': format_type
            },
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()['translatedText']
    
    def detect_language(self, text):
        """Detect the language of the text."""
        response = requests.post(
            f'{self.base_url}/detect',
            json={'q': text},
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()
    
    def get_languages(self):
        """Get list of supported languages."""
        response = requests.get(
            f'{self.base_url}/languages',
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()

# Usage
client = TranslationClient('http://your-server.com:5000')

# Translate
translated = client.translate('Hello, world!', 'en', 'es')
print(translated)  # "¡Hola, mundo!"

# Detect language
detection = client.detect_language('Bonjour')
print(detection)  # {'language': 'fr', 'confidence': 0.95}

# Get languages
languages = client.get_languages()
print(languages)  # [{'code': 'en', 'name': 'English'}, ...]
```

### Flask Integration Example

```python
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
TRANSLATION_API = 'http://your-server.com:5000'

@app.route('/api/translate', methods=['POST'])
def translate():
    data = request.json
    text = data.get('text')
    target_lang = data.get('target_lang', 'es')
    
    # Call your translation server
    response = requests.post(
        f'{TRANSLATION_API}/translate',
        json={
            'q': text,
            'source': 'auto',
            'target': target_lang
        }
    )
    
    if response.status_code == 200:
        return jsonify({
            'success': True,
            'translated': response.json()['translatedText']
        })
    else:
        return jsonify({
            'success': False,
            'error': 'Translation failed'
        }), 500
```

## Node.js Integration

```javascript
const axios = require('axios');

class TranslationClient {
  constructor(baseUrl = 'http://your-server.com:5000', apiKey = null) {
    this.baseUrl = baseUrl;
    this.apiKey = apiKey;
  }

  async translate(text, source = 'auto', target = 'en', format = 'text') {
    const headers = {
      'Content-Type': 'application/json'
    };
    
    if (this.apiKey) {
      headers['X-API-Key'] = this.apiKey;
    }
    
    const response = await axios.post(
      `${this.baseUrl}/translate`,
      {
        q: text,
        source: source,
        target: target,
        format: format
      },
      { headers }
    );
    
    return response.data.translatedText;
  }

  async detectLanguage(text) {
    const headers = {
      'Content-Type': 'application/json'
    };
    
    if (this.apiKey) {
      headers['X-API-Key'] = this.apiKey;
    }
    
    const response = await axios.post(
      `${this.baseUrl}/detect`,
      { q: text },
      { headers }
    );
    
    return response.data;
  }

  async getLanguages() {
    const headers = {};
    if (this.apiKey) {
      headers['X-API-Key'] = this.apiKey;
    }
    
    const response = await axios.get(
      `${this.baseUrl}/languages`,
      { headers }
    );
    
    return response.data;
  }
}

// Usage
const client = new TranslationClient('http://your-server.com:5000');

client.translate('Hello, world!', 'en', 'es')
  .then(translated => console.log(translated))
  .catch(error => console.error('Error:', error));
```

## PHP Integration

```php
<?php
class TranslationClient {
    private $baseUrl;
    private $apiKey;
    
    public function __construct($baseUrl = 'http://your-server.com:5000', $apiKey = null) {
        $this->baseUrl = $baseUrl;
        $this->apiKey = $apiKey;
    }
    
    public function translate($text, $source = 'auto', $target = 'en', $format = 'text') {
        $data = [
            'q' => $text,
            'source' => $source,
            'target' => $target,
            'format' => $format
        ];
        
        $headers = [
            'Content-Type: application/json'
        ];
        
        if ($this->apiKey) {
            $headers[] = 'X-API-Key: ' . $this->apiKey;
        }
        
        $ch = curl_init($this->baseUrl . '/translate');
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
        curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        
        $response = curl_exec($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);
        
        if ($httpCode !== 200) {
            throw new Exception("Translation failed with HTTP $httpCode");
        }
        
        $result = json_decode($response, true);
        return $result['translatedText'];
    }
    
    public function getLanguages() {
        $ch = curl_init($this->baseUrl . '/languages');
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        
        $response = curl_exec($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);
        
        if ($httpCode !== 200) {
            throw new Exception("Failed to get languages");
        }
        
        return json_decode($response, true);
    }
}

// Usage
$client = new TranslationClient('http://your-server.com:5000');
$translated = $client->translate('Hello, world!', 'en', 'es');
echo $translated; // "¡Hola, mundo!"
?>
```

## CORS Configuration

To allow your web apps to access the API from different domains, configure CORS:

**Environment Variable:**
```bash
CORS_ORIGINS=https://myapp.com,https://another-app.com,https://localhost:3000
```

**For development (allow all):**
```bash
CORS_ORIGINS=*
```

**Multiple origins:**
```bash
CORS_ORIGINS=https://app1.com,https://app2.com,http://localhost:3000
```

## API Authentication

If you want to protect your API with authentication:

**Enable API keys:**
```bash
API_KEY_REQUIRED=true
API_KEYS=secret-key-1,secret-key-2,another-key
```

**Using API key in requests:**
```javascript
fetch('http://your-server.com:5000/translate', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-API-Key': 'secret-key-1'  // Add this header
  },
  body: JSON.stringify({...})
});
```

## Error Handling

### Common HTTP Status Codes

- `200` - Success
- `400` - Bad Request (invalid parameters)
- `401` - Unauthorized (API key required/missing)
- `403` - Forbidden (invalid API key)
- `500` - Internal Server Error (translation failed)
- `503` - Service Unavailable (models not loaded)

### JavaScript Error Handling Example

```javascript
async function translateWithErrorHandling(text, source, target) {
  try {
    const response = await fetch('http://your-server.com:5000/translate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ q: text, source, target })
    });
    
    if (response.status === 401) {
      throw new Error('API key required');
    }
    if (response.status === 403) {
      throw new Error('Invalid API key');
    }
    if (response.status === 503) {
      throw new Error('Translation service not available. Please try again later.');
    }
    if (!response.ok) {
      throw new Error(`Translation failed: ${response.statusText}`);
    }
    
    const data = await response.json();
    return data.translatedText;
  } catch (error) {
    if (error.name === 'TypeError' && error.message.includes('fetch')) {
      throw new Error('Cannot connect to translation server');
    }
    throw error;
  }
}
```

## Best Practices

### 1. **Rate Limiting**
Consider implementing rate limiting in your client:
```javascript
class RateLimitedTranslator {
  constructor(apiUrl, maxRequests = 10, windowMs = 60000) {
    this.apiUrl = apiUrl;
    this.requests = [];
    this.maxRequests = maxRequests;
    this.windowMs = windowMs;
  }
  
  async translate(text, source, target) {
    // Remove old requests outside the window
    const now = Date.now();
    this.requests = this.requests.filter(time => now - time < this.windowMs);
    
    if (this.requests.length >= this.maxRequests) {
      throw new Error('Rate limit exceeded. Please wait.');
    }
    
    this.requests.push(now);
    // ... make translation request
  }
}
```

### 2. **Caching Translations**
Cache frequently translated phrases:
```javascript
const translationCache = new Map();

function getCacheKey(text, source, target) {
  return `${source}-${target}-${text}`;
}

async function translateWithCache(text, source, target) {
  const cacheKey = getCacheKey(text, source, target);
  if (translationCache.has(cacheKey)) {
    return translationCache.get(cacheKey);
  }
  
  const translated = await translateText(text, source, target);
  translationCache.set(cacheKey, translated);
  return translated;
}
```

### 3. **Batch Translation**
For multiple texts, translate them sequentially to avoid overwhelming the server:
```javascript
async function translateBatch(texts, source, target) {
  const results = [];
  for (const text of texts) {
    const translated = await translateText(text, source, target);
    results.push(translated);
    // Small delay between requests
    await new Promise(resolve => setTimeout(resolve, 100));
  }
  return results;
}
```

### 4. **Retry Logic**
Implement exponential backoff for retries:
```javascript
async function translateWithRetry(text, source, target, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await translateText(text, source, target);
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      const delay = Math.pow(2, i) * 1000; // Exponential backoff
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }
}
```

## Deployment Tips

1. **Use Environment Variables** for API URL:
   ```javascript
   const API_URL = process.env.REACT_APP_TRANSLATION_API || 'http://localhost:5000';
   ```

2. **Proxy Requests** in development (React/Vue):
   ```json
   // package.json or vite.config.js
   "proxy": "http://your-server.com:5000"
   ```

3. **Handle CORS** properly in production

4. **Monitor API Health**:
   ```javascript
   async function checkHealth() {
     const response = await fetch(`${API_URL}/health`);
     return response.ok;
   }
   ```

## Security Considerations

1. **Enable API Keys** for production
2. **Use HTTPS** for your translation server
3. **Whitelist domains** in CORS_ORIGINS
4. **Validate input** on client side before sending
5. **Sanitize output** before displaying translated text

