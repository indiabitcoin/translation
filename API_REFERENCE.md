# API Reference
## LibreTranslate Self-Hosted Server

**Base URL:** `https://translate.shravani.group/`  
**API Version:** 1.0  
**Protocol:** HTTP/HTTPS  
**Data Format:** JSON

---

## Table of Contents

1. [Authentication](#authentication)
2. [Endpoints](#endpoints)
3. [Request/Response Formats](#requestresponse-formats)
4. [Error Handling](#error-handling)
5. [Rate Limiting](#rate-limiting)
6. [Code Examples](#code-examples)

---

## Authentication

### API Key Authentication

The API supports optional API key authentication. When enabled (`API_KEY_REQUIRED=true`), all requests must include a valid API key.

### Methods

#### 1. Header Method (Recommended)
```http
X-API-Key: your-api-key-here
```

#### 2. Query Parameter Method
```
?api_key=your-api-key-here
```

#### 3. Request Body Method
```json
{
  "api_key": "your-api-key-here",
  ...
}
```

### Generating API Keys

Use the provided script:
```bash
python generate_api_key.py
```

Or generate programmatically:
```python
import secrets
api_key = secrets.token_urlsafe(32)
print(api_key)
```

---

## Endpoints

### 1. Translate Text

Translate text from one language to another.

**Endpoint:** `POST /translate`

**Authentication:** Optional (if `API_KEY_REQUIRED=true`)

**Request:**

```http
POST /translate HTTP/1.1
Host: translate.shravani.group
Content-Type: application/json
X-API-Key: your-api-key-here

{
  "q": "Hello, world!",
  "source": "en",
  "target": "es",
  "format": "text"
}
```

**Request Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `q` | string | ✅ Yes | - | Text to translate |
| `source` | string | ❌ No | `"auto"` | Source language code (ISO 639-1) or `"auto"` for automatic detection |
| `target` | string | ✅ Yes | - | Target language code (ISO 639-1) |
| `format` | string | ❌ No | `"text"` | Format: `"text"` or `"html"` |
| `api_key` | string | ❌ No | - | API key (alternative to header) |

**Response (200 OK):**

```json
{
  "translatedText": "¡Hola, mundo!"
}
```

**Error Responses:**

| Status | Description | Example Response |
|--------|-------------|------------------|
| 400 | Bad Request | `{"detail": "No translation package available for en -> cy"}` |
| 401 | Unauthorized | `{"detail": "Invalid API key"}` |
| 422 | Validation Error | `{"detail": [{"loc": ["body", "q"], "msg": "field required"}]}` |
| 500 | Server Error | `{"detail": "Translation failed: ..."}` |

**Example Requests:**

```bash
# cURL
curl -X POST https://translate.shravani.group/translate \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{
    "q": "Hello, world!",
    "source": "en",
    "target": "es"
  }'

# JavaScript (Fetch API)
const response = await fetch('https://translate.shravani.group/translate', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-API-Key': 'your-api-key'
  },
  body: JSON.stringify({
    q: 'Hello, world!',
    source: 'en',
    target: 'es'
  })
});
const data = await response.json();
console.log(data.translatedText);

# Python (requests)
import requests

response = requests.post(
    'https://translate.shravani.group/translate',
    headers={
        'Content-Type': 'application/json',
        'X-API-Key': 'your-api-key'
    },
    json={
        'q': 'Hello, world!',
        'source': 'en',
        'target': 'es'
    }
)
print(response.json()['translatedText'])
```

---

### 2. Get Supported Languages

Get a list of all supported languages.

**Endpoint:** `GET /languages`

**Authentication:** Optional (if `API_KEY_REQUIRED=true`)

**Request:**

```http
GET /languages HTTP/1.1
Host: translate.shravani.group
X-API-Key: your-api-key-here
```

**Response (200 OK):**

```json
[
  {
    "code": "en",
    "name": "English"
  },
  {
    "code": "es",
    "name": "Spanish"
  },
  {
    "code": "fr",
    "name": "French"
  }
]
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `code` | string | ISO 639-1 language code |
| `name` | string | Human-readable language name |

**Example Requests:**

```bash
# cURL
curl -X GET https://translate.shravani.group/languages \
  -H "X-API-Key: your-api-key"

# JavaScript
const response = await fetch('https://translate.shravani.group/languages', {
  headers: { 'X-API-Key': 'your-api-key' }
});
const languages = await response.json();
console.log(languages);

# Python
import requests

response = requests.get(
    'https://translate.shravani.group/languages',
    headers={'X-API-Key': 'your-api-key'}
)
languages = response.json()
print(languages)
```

---

### 3. Detect Language

Detect the language of the provided text.

**Endpoint:** `POST /detect`

**Authentication:** Optional (if `API_KEY_REQUIRED=true`)

**Request:**

```http
POST /detect HTTP/1.1
Host: translate.shravani.group
Content-Type: application/json
X-API-Key: your-api-key-here

{
  "q": "Bonjour le monde"
}
```

**Request Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `q` | string | ✅ Yes | Text to detect language for |
| `api_key` | string | ❌ No | API key (alternative to header) |

**Response (200 OK):**

```json
{
  "confidence": 0.95,
  "language": "fr"
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `confidence` | float | Confidence score (0.0 to 1.0) |
| `language` | string | Detected language code (ISO 639-1) |

**Example Requests:**

```bash
# cURL
curl -X POST https://translate.shravani.group/detect \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{"q": "Bonjour le monde"}'

# JavaScript
const response = await fetch('https://translate.shravani.group/detect', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-API-Key': 'your-api-key'
  },
  body: JSON.stringify({ q: 'Bonjour le monde' })
});
const data = await response.json();
console.log(`Detected: ${data.language} (confidence: ${data.confidence})`);

# Python
import requests

response = requests.post(
    'https://translate.shravani.group/detect',
    headers={
        'Content-Type': 'application/json',
        'X-API-Key': 'your-api-key'
    },
    json={'q': 'Bonjour le monde'}
)
data = response.json()
print(f"Detected: {data['language']} (confidence: {data['confidence']})")
```

---

### 4. Health Check

Check server health status.

**Endpoint:** `GET /health`

**Authentication:** Not required

**Request:**

```http
GET /health HTTP/1.1
Host: translate.shravani.group
```

**Response (200 OK):**

```json
{
  "status": "ok"
}
```

**Example Request:**

```bash
curl https://translate.shravani.group/health
```

---

### 5. Package Information (Diagnostic)

Get detailed information about installed translation packages.

**Endpoint:** `GET /packages`

**Authentication:** Required (if `API_KEY_REQUIRED=true`)

**Request:**

```http
GET /packages HTTP/1.1
Host: translate.shravani.group
X-API-Key: your-api-key-here
```

**Response (200 OK):**

```json
{
  "total_packages": 54,
  "packages": [
    {
      "from_code": "en",
      "to_code": "es",
      "package_name": "translate-en_es",
      "package_version": "1.0"
    },
    {
      "from_code": "es",
      "to_code": "en",
      "package_name": "translate-es_en",
      "package_version": "1.0"
    }
  ],
  "model_directory": {
    "path": "/app/models",
    "exists": true,
    "is_symlink": false,
    "file_count": 54,
    "argos_packages_dir": "/root/.local/share/argos-translate/packages",
    "argos_dir_exists": true,
    "argos_dir_file_count": 54
  },
  "uk_languages": {
    "cy": false,
    "gd": false,
    "kw": false,
    "gv": false
  }
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `total_packages` | integer | Total number of installed packages |
| `packages` | array | List of package information objects |
| `packages[].from_code` | string | Source language code |
| `packages[].to_code` | string | Target language code |
| `packages[].package_name` | string | Package name |
| `packages[].package_version` | string | Package version |
| `model_directory` | object | Model directory information |
| `uk_languages` | object | UK regional language availability |

---

## Request/Response Formats

### Content Type

All requests must use `Content-Type: application/json` header.

### Language Codes

Language codes follow **ISO 639-1** standard (2-letter codes):

- `en` - English
- `es` - Spanish
- `fr` - French
- `de` - German
- `it` - Italian
- `pt` - Portuguese
- `ru` - Russian
- `zh` - Chinese
- `ja` - Japanese
- `ko` - Korean
- ... (70+ languages supported)

See `/languages` endpoint for complete list.

### Format Options

- `text` - Plain text (default)
- `html` - HTML content (preserves HTML tags)

---

## Error Handling

### Error Response Format

All errors follow this format:

```json
{
  "detail": "Error message description"
}
```

### HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 400 | Bad Request | Invalid request (e.g., unsupported language pair) |
| 401 | Unauthorized | Invalid or missing API key |
| 422 | Unprocessable Entity | Validation error (missing required fields) |
| 500 | Internal Server Error | Server error (translation failed, etc.) |
| 503 | Service Unavailable | Service not initialized |

### Common Error Messages

| Error Message | Cause | Solution |
|--------------|-------|----------|
| `"Invalid API key"` | API key missing or incorrect | Check API key in header or request body |
| `"No translation package available for X -> Y"` | Language pair not installed | Check `/languages` endpoint, install model if needed |
| `"Translation failed: ..."` | Internal translation error | Check server logs, verify model installation |
| `"field required"` | Missing required parameter | Include all required fields in request |

### Error Handling Best Practices

```javascript
// JavaScript example
async function translate(text, source, target) {
  try {
    const response = await fetch('https://translate.shravani.group/translate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': process.env.API_KEY
      },
      body: JSON.stringify({ q: text, source, target })
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || `HTTP ${response.status}`);
    }
    
    const data = await response.json();
    return data.translatedText;
  } catch (error) {
    console.error('Translation error:', error);
    throw error;
  }
}
```

---

## Rate Limiting

**Current Status:** No rate limiting implemented at application level.

**Recommendations:**
- Implement rate limiting at reverse proxy level (nginx, Cloudflare)
- Or implement application-level rate limiting for production use
- Monitor API usage for abuse

---

## Code Examples

### JavaScript/TypeScript

```javascript
// Translation client class
class TranslationClient {
  constructor(apiUrl, apiKey) {
    this.apiUrl = apiUrl;
    this.apiKey = apiKey;
  }
  
  async translate(text, source, target) {
    const response = await fetch(`${this.apiUrl}/translate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': this.apiKey
      },
      body: JSON.stringify({
        q: text,
        source: source || 'auto',
        target: target
      })
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail);
    }
    
    const data = await response.json();
    return data.translatedText;
  }
  
  async getLanguages() {
    const response = await fetch(`${this.apiUrl}/languages`, {
      headers: { 'X-API-Key': this.apiKey }
    });
    return response.json();
  }
  
  async detectLanguage(text) {
    const response = await fetch(`${this.apiUrl}/detect`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': this.apiKey
      },
      body: JSON.stringify({ q: text })
    });
    return response.json();
  }
}

// Usage
const client = new TranslationClient(
  'https://translate.shravani.group',
  'your-api-key'
);

const translated = await client.translate('Hello', 'en', 'es');
console.log(translated); // "Hola"
```

### Python

```python
import requests
from typing import Optional, Dict, List

class TranslationClient:
    def __init__(self, api_url: str, api_key: Optional[str] = None):
        self.api_url = api_url.rstrip('/')
        self.api_key = api_key
        self.headers = {'Content-Type': 'application/json'}
        if api_key:
            self.headers['X-API-Key'] = api_key
    
    def translate(
        self,
        text: str,
        source: str = 'auto',
        target: str = 'en',
        format_type: str = 'text'
    ) -> str:
        """Translate text from source to target language."""
        response = requests.post(
            f'{self.api_url}/translate',
            headers=self.headers,
            json={
                'q': text,
                'source': source,
                'target': target,
                'format': format_type
            }
        )
        response.raise_for_status()
        return response.json()['translatedText']
    
    def get_languages(self) -> List[Dict[str, str]]:
        """Get list of supported languages."""
        response = requests.get(
            f'{self.api_url}/languages',
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()
    
    def detect_language(self, text: str) -> Dict[str, any]:
        """Detect language of text."""
        response = requests.post(
            f'{self.api_url}/detect',
            headers=self.headers,
            json={'q': text}
        )
        response.raise_for_status()
        return response.json()

# Usage
client = TranslationClient(
    'https://translate.shravani.group',
    api_key='your-api-key'
)

translated = client.translate('Hello', 'en', 'es')
print(translated)  # "Hola"
```

### Node.js/Express

```javascript
const axios = require('axios');

class TranslationService {
  constructor(apiUrl, apiKey) {
    this.client = axios.create({
      baseURL: apiUrl,
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': apiKey
      }
    });
  }
  
  async translate(text, source, target) {
    const response = await this.client.post('/translate', {
      q: text,
      source: source || 'auto',
      target: target
    });
    return response.data.translatedText;
  }
  
  async getLanguages() {
    const response = await this.client.get('/languages');
    return response.data;
  }
}

// Express route example
app.post('/api/translate', async (req, res) => {
  try {
    const { text, source, target } = req.body;
    const service = new TranslationService(
      process.env.TRANSLATE_API_URL,
      process.env.TRANSLATE_API_KEY
    );
    const translated = await service.translate(text, source, target);
    res.json({ translated });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});
```

---

## Best Practices

1. **Always check available languages** before attempting translation
2. **Handle errors gracefully** - provide fallback behavior
3. **Cache language lists** - they don't change frequently
4. **Use environment variables** for API keys (never hardcode)
5. **Implement retry logic** for transient failures
6. **Monitor API usage** for performance and cost tracking
7. **Validate input** before sending to API
8. **Use HTTPS** in production environments

---

## Support

- **Documentation:** See README.md and other .md files
- **GitHub:** https://github.com/indiabitcoin/translation
- **Live Server:** https://translate.shravani.group/

---

**Last Updated:** December 2024  
**API Version:** 1.0

