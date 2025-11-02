# LibreTranslate Self-Hosted Server

A self-hosted translation server built with LibreTranslate API, providing REST endpoints for machine translation. Perfect for integrating translation capabilities into multiple web applications and websites.

🌐 **Live Server**: https://translate.shravani.group/

## Features

- 🌐 RESTful API for translation services
- 🔄 Support for multiple languages
- 🚀 Fast and efficient translation using Argos Translate (the engine behind LibreTranslate)
- 🔒 Optional API key authentication
- 📦 Docker support
- ⚙️ Configurable via environment variables

## Installation

### Prerequisites

- Python 3.8, 3.9, or 3.10
- pip

### Setup

1. Clone or navigate to this repository:
```bash
cd LibreTranslate
```

2. Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Copy environment file and configure:
```bash
cp .env.example .env
# Edit .env with your preferred settings
```

## Usage

### Running the Server

#### Basic Usage
```bash
python main.py
```

#### With Custom Configuration
```bash
# Load specific languages only (faster startup)
LOAD_ONLY=en,es,fr python main.py

# Update translation models
UPDATE_MODELS=true python main.py
```

### Docker Usage

#### Build the Docker image:
```bash
docker build -t libretranslate-server .
```

#### Run the container:
```bash
docker run -p 5000:5000 libretranslate-server
```

## API Endpoints

### Translate Text
```http
POST /translate
Content-Type: application/json

{
  "q": "Hello, world!",
  "source": "en",
  "target": "es",
  "format": "text"
}
```

Response:
```json
{
  "translatedText": "¡Hola, mundo!"
}
```

### Get Supported Languages
```http
GET /languages
```

Response:
```json
[
  {
    "code": "en",
    "name": "English"
  },
  {
    "code": "es",
    "name": "Spanish"
  }
]
```

### Detect Language
```http
POST /detect
Content-Type: application/json

{
  "q": "Hello, world!"
}
```

Response:
```json
{
  "confidence": 0.95,
  "language": "en"
}
```

### Health Check
```http
GET /health
```

Response:
```json
{
  "status": "ok"
}
```

## Deployment to Coolify

This server is optimized for Coolify deployment with a 500MB repository limit. **Translation models are downloaded at runtime**, not bundled in the Docker image, keeping your repository small.

See **[COOLIFY_DEPLOYMENT.md](COOLIFY_DEPLOYMENT.md)** for detailed deployment instructions.

**Quick Summary:**
- Repository size: ~20MB (code only, no models) ✓
- Models download on first container start
- Models stored in persistent volume (`/app/models`)
- Use `LOAD_ONLY` environment variable to limit languages
- Set `UPDATE_MODELS=true` on first deployment

## Configuration

Environment variables can be set in the `.env` file:

- `HOST`: Server host (default: `0.0.0.0`)
- `PORT`: Server port (default: `5000`)
- `LOAD_ONLY`: Comma-separated language codes to load (e.g., `en,es,fr`)
- `UPDATE_MODELS`: Whether to update translation models on startup (default: `false`)
- `API_KEY_REQUIRED`: Require API key for requests (default: `false`)
- `API_KEYS`: Comma-separated list of valid API keys
- `CORS_ORIGINS`: CORS allowed origins (default: `*`)
- `ARGOS_TRANSLATE_PACKAGES`: Custom directory for models (default: `/app/models` for Docker)

## Integration with Web Apps

This translation server can be easily integrated into any web application or website. See **[INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)** for comprehensive examples including:

- **JavaScript/React/Vue** integration examples
- **Python** backend integration
- **Node.js** integration
- **PHP** integration
- **Complete widget examples**
- **CORS configuration**
- **API authentication**
- **Error handling patterns**

### Quick Integration Example

```javascript
// Simple JavaScript integration
async function translate(text, targetLang) {
  const response = await fetch('http://your-server.com:5000/translate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      q: text,
      source: 'auto',
      target: targetLang
    })
  });
  const data = await response.json();
  return data.translatedText;
}

// Usage
translate('Hello, world!', 'es').then(result => console.log(result));
```

### Ready-to-Use Widget

Check out `examples/simple-widget.html` for a complete, production-ready translation widget that you can embed in any website.

### Real-Time Website Translation

**Yes, you can use the translation server URL as a backend API for real-time translation!**

Your websites can communicate with the translation server to:
- Translate page content on-the-fly
- Translate user comments/posts in real-time
- Provide click-to-translate functionality
- Auto-translate entire sections
- Translate dynamic/AJAX content

See **[examples/WEBSITE_INTEGRATION.md](examples/WEBSITE_INTEGRATION.md)** for complete examples and patterns.

**Quick Example:**
```javascript
// Translate any element in real-time
async function translateElement(element, targetLang) {
    const response = await fetch('http://your-server.com:5000/translate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            q: element.textContent,
            source: 'auto',
            target: targetLang
        })
    });
    const data = await response.json();
    element.textContent = data.translatedText;
}
```

## Development

### Project Structure
```
LibreTranslate/
├── main.py                 # FastAPI application entry point
├── app/
│   ├── __init__.py
│   ├── config.py          # Configuration management
│   ├── translation.py     # Translation service
│   └── models.py          # Pydantic models
├── examples/              # Integration examples
│   ├── simple-widget.html      # Complete translation widget
│   ├── translation-client.js   # Reusable JavaScript client
│   └── QUICK_REFERENCE.md      # Quick API reference
├── requirements.txt       # Python dependencies
├── start.sh              # Startup script (model installation)
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose config
├── INTEGRATION_GUIDE.md  # Complete integration guide
├── COOLIFY_DEPLOYMENT.md # Coolify deployment guide
└── README.md             # This file
```

## Notes

- On first run, you may need to download translation models. Set `UPDATE_MODELS=true` to automatically download models, or run:
  ```bash
  python -m argostranslate.update
  ```
- Translation models are stored in `~/.local/share/argos-translate/packages`
- The server will only support languages for which translation models are installed

## License

This project uses Argos Translate, which is licensed under the AGPL-3.0 license.

