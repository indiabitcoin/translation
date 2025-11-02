# Website Integration Guide: Real-Time Translation

This guide shows how to use your translation server URL as a backend API to translate website content in real-time.

## Overview

Your translation server can be used as a backend API that websites communicate with to:
- ✅ Translate page content on-the-fly
- ✅ Translate user comments/posts in real-time
- ✅ Translate forms and user inputs
- ✅ Provide inline translation on hover/click
- ✅ Auto-translate entire page sections
- ✅ Translate dynamic content (AJAX-loaded)

## Quick Setup

### Step 1: Configure CORS on Your Server

Allow your website domains to access the API:

```bash
CORS_ORIGINS=https://yourwebsite.com,https://another-site.com,http://localhost:3000
```

### Step 2: Include the Translation Client

Add to your website's HTML:

```html
<!-- Option 1: Use the reusable client -->
<script src="https://your-cdn.com/translation-client.js"></script>

<!-- Option 2: Use inline translator for click-to-translate -->
<script src="https://your-cdn.com/inline-translator.js"></script>
```

### Step 3: Use the API

```javascript
const client = new TranslationClient('http://your-server.com:5000');

// Translate any text
const translated = await client.translate('Hello, world!', 'en', 'es');
console.log(translated); // "¡Hola, mundo!"
```

## Integration Patterns

### Pattern 1: Translate Page on Button Click

Perfect for: Blogs, news sites, documentation

```html
<button onclick="translatePage('es')">Translate to Spanish</button>

<script>
async function translatePage(targetLang) {
    const elements = document.querySelectorAll('[data-translate]');
    
    for (const element of elements) {
        const original = element.textContent;
        const translated = await fetch('http://your-server.com:5000/translate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                q: original,
                source: 'auto',
                target: targetLang
            })
        }).then(r => r.json());
        
        element.textContent = translated.translatedText;
    }
}
</script>
```

**Usage:**
```html
<article data-translate>
    <h1>Welcome to Our Blog</h1>
    <p>This content will be translated when you click the button.</p>
</article>
```

### Pattern 2: Translate User Comments in Real-Time

Perfect for: Forums, social media, review sites

```javascript
function translateComment(commentElement, targetLang) {
    const commentText = commentElement.querySelector('.comment-text');
    const original = commentText.textContent;
    
    // Show loading
    commentText.innerHTML = '<em>Translating...</em>';
    
    fetch('http://your-server.com:5000/translate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            q: original,
            source: 'auto',
            target: targetLang
        })
    })
    .then(r => r.json())
    .then(data => {
        commentText.textContent = data.translatedText;
        commentText.setAttribute('data-translated', targetLang);
        commentText.setAttribute('data-original', original);
    });
}

// Add translate button to each comment
document.querySelectorAll('.comment').forEach(comment => {
    const btn = document.createElement('button');
    btn.textContent = 'Translate';
    btn.onclick = () => translateComment(comment, 'es');
    comment.appendChild(btn);
});
```

### Pattern 3: Click-to-Translate Any Element

Perfect for: E-commerce, FAQs, documentation

**Using inline-translator.js:**
```html
<p data-translate="true">Click this text to translate it!</p>
<p class="translate-on-click">Or add this class to any element</p>

<script src="inline-translator.js"></script>
<script>
    // Configure
    InlineTranslator.setApiUrl('http://your-server.com:5000');
    InlineTranslator.setLanguage('es'); // Default target
</script>
```

**Manual implementation:**
```javascript
document.querySelectorAll('.click-to-translate').forEach(element => {
    element.addEventListener('click', async function() {
        const original = this.textContent;
        const response = await fetch('http://your-server.com:5000/translate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                q: original,
                source: 'auto',
                target: 'es'
            })
        });
        const data = await response.json();
        this.textContent = data.translatedText;
    });
});
```

### Pattern 4: Auto-Translate on Form Submit

Perfect for: Contact forms, search boxes, chatbots

```html
<form onsubmit="translateForm(event)">
    <input type="text" id="message" placeholder="Type a message...">
    <select id="lang">
        <option value="es">Spanish</option>
        <option value="fr">French</option>
    </select>
    <button type="submit">Send Translated</button>
</form>

<script>
async function translateForm(event) {
    event.preventDefault();
    const message = document.getElementById('message').value;
    const targetLang = document.getElementById('lang').value;
    
    // Translate before sending
    const response = await fetch('http://your-server.com:5000/translate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            q: message,
            source: 'auto',
            target: targetLang
        })
    });
    
    const data = await response.json();
    
    // Send translated message to your backend
    // ... your submission logic
    console.log('Sending:', data.translatedText);
}
</script>
```

### Pattern 5: Language Switcher Widget

Perfect for: Multi-language website support

```html
<div class="lang-switcher">
    <select id="langSelect" onchange="switchLanguage(this.value)">
        <option value="">Select Language</option>
        <option value="es">Español</option>
        <option value="fr">Français</option>
        <option value="de">Deutsch</option>
    </select>
</div>

<script>
let currentLang = null;
let originalTexts = new Map();

async function switchLanguage(targetLang) {
    if (!targetLang) return;
    
    // Store original texts on first translation
    if (!currentLang) {
        document.querySelectorAll('[data-translatable]').forEach(el => {
            originalTexts.set(el, el.textContent);
        });
    }
    
    // Translate all translatable elements
    const elements = document.querySelectorAll('[data-translatable]');
    
    for (const element of elements) {
        const original = originalTexts.get(element);
        
        const response = await fetch('http://your-server.com:5000/translate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                q: original,
                source: 'auto',
                target: targetLang
            })
        });
        
        const data = await response.json();
        element.textContent = data.translatedText;
    }
    
    currentLang = targetLang;
    
    // Save preference
    localStorage.setItem('preferredLang', targetLang);
}

// Restore language preference
window.addEventListener('DOMContentLoaded', () => {
    const saved = localStorage.getItem('preferredLang');
    if (saved) {
        document.getElementById('langSelect').value = saved;
        switchLanguage(saved);
    }
});
</script>
```

### Pattern 6: Translate Dynamic Content (AJAX)

Perfect for: Single-page apps, infinite scroll, live updates

```javascript
// Override fetch or use interceptors to auto-translate responses
const originalFetch = window.fetch;
window.fetch = async function(...args) {
    const response = await originalFetch(...args);
    
    // Clone response to read it
    const cloned = response.clone();
    const data = await cloned.json();
    
    // If response contains text to translate
    if (data.content) {
        const translated = await translateText(data.content, 'auto', 'es');
        data.content = translated;
    }
    
    // Return modified response
    return new Response(JSON.stringify(data), {
        status: response.status,
        headers: response.headers
    });
};

async function translateText(text, source, target) {
    const response = await fetch('http://your-server.com:5000/translate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ q: text, source, target })
    });
    return (await response.json()).translatedText;
}
```

## Complete Example: Real-Time Blog Translation

```html
<!DOCTYPE html>
<html>
<head>
    <title>My Blog</title>
    <style>
        .translate-btn {
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 10px 20px;
            background: #007bff;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <button class="translate-btn" onclick="translatePage()">🌐 Translate</button>
    
    <article>
        <h1 data-translate>Welcome to My Blog</h1>
        <p data-translate>
            This is a sample blog post that can be translated in real-time
            using the translation API.
        </p>
    </article>

    <script>
        const API_URL = 'http://your-server.com:5000';
        let translated = false;
        let originalTexts = new Map();

        async function translatePage() {
            const targetLang = prompt('Enter language code (es, fr, de, etc.):', 'es');
            if (!targetLang) return;

            // Store originals on first translation
            if (!translated) {
                document.querySelectorAll('[data-translate]').forEach(el => {
                    originalTexts.set(el, el.textContent);
                });
            }

            // Translate all elements
            for (const [element, original] of originalTexts) {
                const response = await fetch(`${API_URL}/translate`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        q: original,
                        source: 'auto',
                        target: targetLang
                    })
                });
                
                const data = await response.json();
                element.textContent = data.translatedText;
            }

            translated = true;
            document.querySelector('.translate-btn').textContent = '↺ Reset';
            document.querySelector('.translate-btn').onclick = resetPage;
        }

        function resetPage() {
            for (const [element, original] of originalTexts) {
                element.textContent = original;
            }
            translated = false;
            document.querySelector('.translate-btn').textContent = '🌐 Translate';
            document.querySelector('.translate-btn').onclick = translatePage;
        }
    </script>
</body>
</html>
```

## Best Practices

### 1. **Cache Translations**
```javascript
const cache = new Map();

async function translate(text, lang) {
    const key = `${lang}-${text}`;
    if (cache.has(key)) return cache.get(key);
    
    const result = await fetch(/* ... */).then(r => r.json());
    cache.set(key, result.translatedText);
    return result.translatedText;
}
```

### 2. **Show Loading States**
```javascript
element.textContent = 'Translating...';
element.style.opacity = '0.5';
// ... translate
element.style.opacity = '1';
```

### 3. **Handle Errors Gracefully**
```javascript
try {
    const translated = await translate(text, lang);
    element.textContent = translated;
} catch (error) {
    console.error('Translation failed:', error);
    // Keep original text
}
```

### 4. **Rate Limiting**
Don't send too many requests at once:
```javascript
async function translateBatch(elements, lang) {
    for (const element of elements) {
        await translateElement(element, lang);
        await new Promise(r => setTimeout(r, 100)); // 100ms delay
    }
}
```

## Security Considerations

1. **Use HTTPS** for your translation server in production
2. **Enable API Keys** for protection:
   ```bash
   API_KEY_REQUIRED=true
   API_KEYS=your-secret-key
   ```
3. **Whitelist domains** in CORS_ORIGINS
4. **Validate input** before sending to API
5. **Sanitize output** before displaying

## Example Files

- `page-translator.html` - Complete page translation example
- `realtime-translation.js` - Reusable translation utilities
- `inline-translator.js` - Click-to-translate script
- `translation-client.js` - Full-featured API client

## Next Steps

1. Deploy your translation server
2. Configure CORS for your domains
3. Choose an integration pattern that fits your needs
4. Test with real content
5. Enable API keys for production use

Your translation server is now ready to power real-time translations across all your websites! 🚀

