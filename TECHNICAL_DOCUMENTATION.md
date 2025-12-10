# Technical Documentation
## LibreTranslate Self-Hosted Server

**Version:** 1.0  
**Last Updated:** December 2024  
**Server URL:** https://translate.shravani.group/

---

## Table of Contents

1. [System Architecture](#system-architecture)
2. [API Reference](#api-reference)
3. [Technical Specifications](#technical-specifications)
4. [Deployment Architecture](#deployment-architecture)
5. [Security Architecture](#security-architecture)
6. [Performance Characteristics](#performance-characteristics)
7. [System Requirements](#system-requirements)
8. [Troubleshooting](#troubleshooting)

---

## System Architecture

### Overview

The LibreTranslate server is a RESTful API service built on FastAPI (Python) that provides machine translation capabilities using Argos Translate, an open-source neural machine translation engine.

### Component Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Client Applications                        │
│  (Web Apps, Mobile Apps, Backend Services, Websites)          │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP/REST API
                       │ (JSON)
┌──────────────────────▼──────────────────────────────────────┐
│                    FastAPI Application                        │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  API Endpoints                                        │   │
│  │  - /translate                                         │   │
│  │  - /languages                                         │   │
│  │  - /detect                                            │   │
│  │  - /health                                            │   │
│  │  - /packages (diagnostic)                             │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Authentication Layer                                 │   │
│  │  - API Key Validation                                 │   │
│  │  - CORS Handling                                      │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Translation Service                                  │   │
│  │  - Language Detection                                 │   │
│  │  - Translation Processing                             │   │
│  │  - Model Management                                   │   │
│  └──────────────────────────────────────────────────────┘   │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│              Argos Translate Engine                          │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Neural Translation Models                             │   │
│  │  - Pre-trained language pair models                    │   │
│  │  - Community models                                    │   │
│  │  - Model storage: /app/models                          │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Web Framework** | FastAPI | Latest |
| **Python** | Python | 3.8+ |
| **Translation Engine** | Argos Translate | Latest |
| **HTTP Server** | Uvicorn | Latest |
| **Validation** | Pydantic | Latest |
| **Containerization** | Docker | Latest |
| **Deployment** | Coolify/Nixpacks | Latest |

### Data Flow

1. **Request Reception**: FastAPI receives HTTP POST/GET request
2. **Authentication**: API key validated (if enabled)
3. **Request Validation**: Pydantic models validate request structure
4. **Language Detection**: If `source="auto"`, language is detected
5. **Translation**: Argos Translate engine processes translation
6. **Response**: JSON response returned to client

---

## API Reference

### Base URL

```
Production: https://translate.shravani.group/
Development: http://localhost:3000
```

### Authentication

**Header-based API Key Authentication** (optional, configurable)

```http
X-API-Key: your-api-key-here
```

**Query Parameter** (alternative method)

```
?api_key=your-api-key-here
```

### Endpoints

#### 1. Translate Text

**Endpoint:** `POST /translate`

**Description:** Translates text from source language to target language.

**Request Headers:**
```http
Content-Type: application/json
X-API-Key: <your-api-key> (optional)
```

**Request Body:**
```json
{
  "q": "Hello, world!",
  "source": "en",
  "target": "es",
  "format": "text",
  "api_key": "optional-api-key"
}
```

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `q` | string | Yes | - | Text to translate |
| `source` | string | No | `"auto"` | Source language code or `"auto"` for detection |
| `target` | string | Yes | - | Target language code |
| `format` | string | No | `"text"` | Format: `"text"` or `"html"` |
| `api_key` | string | No | - | API key (if not in header) |

**Response (200 OK):**
```json
{
  "translatedText": "¡Hola, mundo!"
}
```

**Error Responses:**

| Status Code | Description | Example |
|-------------|-------------|---------|
| 400 | Bad Request - Invalid language pair or missing parameters | `{"detail": "No translation package available for en -> cy"}` |
| 401 | Unauthorized - Invalid or missing API key | `{"detail": "Invalid API key"}` |
| 500 | Internal Server Error | `{"detail": "Translation failed: ..."}` |

**Example cURL:**
```bash
curl -X POST https://translate.shravani.group/translate \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{
    "q": "Hello, world!",
    "source": "en",
    "target": "es"
  }'
```

---

#### 2. Get Supported Languages

**Endpoint:** `GET /languages`

**Description:** Returns list of all supported languages with codes and names.

**Request Headers:**
```http
X-API-Key: <your-api-key> (optional)
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

**Example cURL:**
```bash
curl -X GET https://translate.shravani.group/languages \
  -H "X-API-Key: your-api-key"
```

---

#### 3. Detect Language

**Endpoint:** `POST /detect`

**Description:** Detects the language of the provided text.

**Request Headers:**
```http
Content-Type: application/json
X-API-Key: <your-api-key> (optional)
```

**Request Body:**
```json
{
  "q": "Bonjour le monde",
  "api_key": "optional-api-key"
}
```

**Response (200 OK):**
```json
{
  "confidence": 0.95,
  "language": "fr"
}
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `q` | string | Yes | Text to detect language for |
| `api_key` | string | No | API key (if not in header) |

**Example cURL:**
```bash
curl -X POST https://translate.shravani.group/detect \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{"q": "Bonjour le monde"}'
```

---

#### 4. Health Check

**Endpoint:** `GET /health`

**Description:** Returns server health status.

**Response (200 OK):**
```json
{
  "status": "ok"
}
```

**Example cURL:**
```bash
curl https://translate.shravani.group/health
```

---

#### 5. Package Information (Diagnostic)

**Endpoint:** `GET /packages`

**Description:** Returns detailed information about installed translation packages (diagnostic endpoint).

**Request Headers:**
```http
X-API-Key: <your-api-key> (required if API_KEY_REQUIRED=true)
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

---

## Technical Specifications

### Language Support

**Default Installation:** 70+ languages

**Full Installation:** 100+ languages (with `INSTALL_ALL_LANGUAGES=true`)

**Language Categories:**
- European Languages (32 languages)
- Major World Languages (20+ languages)
- Regional Languages (20+ languages)
- Community Models (varies)

### Model Specifications

- **Model Format:** Argos Translate package format (`.argosmodel`)
- **Model Size:** 50-500MB per language pair
- **Storage Location:** `/app/models` (configurable via `ARGOS_TRANSLATE_PACKAGES`)
- **Total Storage:** ~10-50GB for full language set

### Performance Metrics

| Metric | Value |
|--------|-------|
| **Average Translation Time** | 50-200ms per request |
| **Throughput** | 50-100 requests/second (single instance) |
| **Concurrent Requests** | Limited by server resources |
| **Model Load Time** | 1-3 seconds per model (first use) |
| **Memory Usage** | 500MB-2GB (depending on loaded models) |

### API Rate Limits

Currently **no rate limiting** implemented. Recommended:
- Implement rate limiting at reverse proxy level (nginx, Cloudflare)
- Or implement application-level rate limiting for production use

---

## Deployment Architecture

### Container Architecture

```
┌─────────────────────────────────────────┐
│         Docker Container                 │
│  ┌───────────────────────────────────┐  │
│  │  FastAPI Application              │  │
│  │  - Uvicorn ASGI Server            │  │
│  │  - Port: 3000 (internal)          │  │
│  └───────────────────────────────────┘  │
│  ┌───────────────────────────────────┐  │
│  │  Argos Translate                   │  │
│  │  - Translation Models              │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
         │
         │ Persistent Volume
         ▼
┌─────────────────────────────────────────┐
│    /app/models (Persistent Storage)      │
│  - Translation model packages            │
│  - Survives container restarts           │
└─────────────────────────────────────────┘
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `HOST` | `0.0.0.0` | Server bind address |
| `PORT` | `3000` | Server port |
| `LOAD_ONLY` | - | Comma-separated language codes to load |
| `UPDATE_MODELS` | `false` | Update models on startup |
| `INSTALL_ALL_LANGUAGES` | `false` | Install all available languages |
| `API_KEY_REQUIRED` | `false` | Require API key authentication |
| `API_KEYS` | - | Comma-separated valid API keys |
| `CORS_ORIGINS` | `*` | CORS allowed origins |
| `ARGOS_TRANSLATE_PACKAGES` | `/app/models` | Model storage directory |
| `AUTO_INSTALL_MODELS` | `true` | Auto-install if no models found |

### Deployment Platforms

**Supported:**
- Coolify (recommended)
- Docker/Docker Compose
- Kubernetes
- Any container orchestration platform

**Requirements:**
- Persistent volume for models
- Minimum 2GB RAM
- Minimum 20GB storage (for full language set)

---

## Security Architecture

### Authentication Methods

1. **API Key Authentication** (Header)
   ```http
   X-API-Key: <key>
   ```

2. **API Key Authentication** (Query Parameter)
   ```
   ?api_key=<key>
   ```

3. **API Key Authentication** (Request Body)
   ```json
   {"api_key": "<key>"}
   ```

### Security Features

- **API Key Validation**: Configurable API key requirement
- **CORS Support**: Configurable CORS origins
- **Input Validation**: Pydantic model validation
- **Error Handling**: Secure error messages (no sensitive data leakage)

### Security Best Practices

1. **Enable API Key Authentication** in production
2. **Use HTTPS** (configure at reverse proxy/load balancer)
3. **Restrict CORS Origins** to specific domains
4. **Store API Keys** in environment variables (never hardcode)
5. **Rotate API Keys** periodically
6. **Monitor API Usage** for suspicious activity

### API Key Generation

```bash
python generate_api_key.py
```

Generates a cryptographically secure 32-byte API key.

---

## Performance Characteristics

### Translation Speed

- **Short text (< 100 chars)**: 50-100ms
- **Medium text (100-1000 chars)**: 100-200ms
- **Long text (> 1000 chars)**: 200-500ms

### Scalability

**Horizontal Scaling:**
- Stateless API design allows multiple instances
- Load balancer can distribute requests
- Shared model storage (via persistent volume)

**Vertical Scaling:**
- More RAM = more models loaded in memory
- More CPU = faster translation processing

### Optimization Tips

1. **Limit Languages**: Use `LOAD_ONLY` to load only needed languages
2. **Model Caching**: Models are cached in memory after first use
3. **Batch Processing**: Process multiple translations in parallel
4. **CDN/Reverse Proxy**: Use caching for static responses

---

## System Requirements

### Minimum Requirements

- **CPU**: 2 cores
- **RAM**: 2GB
- **Storage**: 20GB (for models)
- **Network**: 100Mbps

### Recommended Requirements

- **CPU**: 4+ cores
- **RAM**: 4GB+
- **Storage**: 50GB+ (for full language set)
- **Network**: 1Gbps

### Software Requirements

- **Python**: 3.8, 3.9, 3.10, or 3.12
- **Docker**: Latest (for containerized deployment)
- **Operating System**: Linux (recommended), macOS, Windows

---

## Troubleshooting

### Common Issues

#### 1. Models Not Detected

**Symptoms:** "No translation packages installed" warning

**Solutions:**
- Check model directory: `/app/models`
- Verify symlink: `~/.local/share/argos-translate/packages`
- Set `UPDATE_MODELS=true` and restart
- Check `/packages` endpoint for diagnostic info

#### 2. Translation Fails for Specific Language

**Symptoms:** "No translation package available" error

**Solutions:**
- Check if language is in supported list: `/languages`
- Install community model if available
- Verify language code is correct (ISO 639-1)

#### 3. API Key Authentication Not Working

**Symptoms:** "Invalid API key" error

**Solutions:**
- Verify `API_KEY_REQUIRED=true` is set
- Check `API_KEYS` environment variable format (comma-separated)
- Ensure API key is sent in header: `X-API-Key`
- Check for whitespace in API key

#### 4. High Memory Usage

**Symptoms:** Container OOM (Out of Memory)

**Solutions:**
- Reduce languages with `LOAD_ONLY`
- Increase container memory limit
- Unload unused models (restart container)

#### 5. Slow Translation

**Symptoms:** Translation takes > 1 second

**Solutions:**
- Check server CPU usage
- Verify models are loaded (not downloading)
- Reduce text length or batch size
- Scale horizontally (multiple instances)

### Diagnostic Commands

```bash
# Check installed packages
curl http://localhost:3000/packages

# Check health
curl http://localhost:3000/health

# Check available languages
curl http://localhost:3000/languages

# Test translation
curl -X POST http://localhost:3000/translate \
  -H "Content-Type: application/json" \
  -d '{"q": "Hello", "source": "en", "target": "es"}'
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Dec 2024 | Initial release with 70+ languages, API key auth, diagnostic endpoints |

---

## Support & Resources

- **GitHub Repository**: https://github.com/indiabitcoin/translation
- **Live Server**: https://translate.shravani.group/
- **Documentation**: See README.md and other .md files
- **Argos Translate**: https://github.com/argosopentech/argos-translate

---

**Document Status:** Active  
**Maintained By:** Development Team  
**Last Review:** December 2024

