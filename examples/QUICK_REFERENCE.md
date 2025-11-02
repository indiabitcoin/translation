# Quick Reference: Translation API

## Base URL
```
http://your-server.com:5000
```

## Endpoints

### Translate Text
```http
POST /translate
Content-Type: application/json
X-API-Key: your-api-key (optional)

{
  "q": "Hello, world!",
  "source": "en",
  "target": "es",
  "format": "text"
}
```

**Response:**
```json
{
  "translatedText": "¡Hola, mundo!"
}
```

### Get Languages
```http
GET /languages
```

**Response:**
```json
[
  {"code": "en", "name": "English"},
  {"code": "es", "name": "Spanish"},
  ...
]
```

### Detect Language
```http
POST /detect
Content-Type: application/json

{
  "q": "Bonjour"
}
```

**Response:**
```json
{
  "language": "fr",
  "confidence": 0.95
}
```

### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "ok"
}
```

## JavaScript Quick Example

```javascript
// Simple translation function
async function translate(text, from, to) {
  const res = await fetch('http://your-server.com:5000/translate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ q: text, source: from, target: to })
  });
  return (await res.json()).translatedText;
}

// Usage
const result = await translate('Hello', 'en', 'es');
console.log(result); // "Hola"
```

## Python Quick Example

```python
import requests

def translate(text, source='auto', target='en'):
    response = requests.post(
        'http://your-server.com:5000/translate',
        json={'q': text, 'source': source, 'target': target}
    )
    return response.json()['translatedText']

# Usage
result = translate('Hello', 'en', 'es')
print(result)  # "Hola"
```

## Language Codes

Common codes:
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
- `ar` - Arabic
- `hi` - Hindi

Use `auto` for automatic source language detection.

## Error Codes

- `200` - Success
- `400` - Bad Request
- `401` - Unauthorized (API key required)
- `403` - Forbidden (invalid API key)
- `500` - Internal Server Error
- `503` - Service Unavailable

## CORS Configuration

To allow your domain to access the API:

```bash
CORS_ORIGINS=https://myapp.com,https://another-app.com
```

For development:
```bash
CORS_ORIGINS=*
```

## API Authentication

Enable in environment:
```bash
API_KEY_REQUIRED=true
API_KEYS=key1,key2,key3
```

Include in requests:
```javascript
headers: {
  'Content-Type': 'application/json',
  'X-API-Key': 'key1'
}
```

