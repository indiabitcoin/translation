/**
 * Translation API Client
 * 
 * A reusable JavaScript client for the LibreTranslate API
 * Can be used in browsers or Node.js environments
 */

class TranslationClient {
  constructor(baseUrl, apiKey = null) {
    this.baseUrl = baseUrl.replace(/\/$/, ''); // Remove trailing slash
    this.apiKey = apiKey;
  }

  /**
   * Translate text from source language to target language
   * @param {string} text - Text to translate
   * @param {string} source - Source language code or 'auto'
   * @param {string} target - Target language code
   * @param {string} format - Format ('text' or 'html')
   * @returns {Promise<string>} Translated text
   */
  async translate(text, source = 'auto', target = 'en', format = 'text') {
    if (!text || !text.trim()) {
      throw new Error('Text to translate cannot be empty');
    }

    const headers = {
      'Content-Type': 'application/json'
    };

    if (this.apiKey) {
      headers['X-API-Key'] = this.apiKey;
    }

    try {
      const response = await fetch(`${this.baseUrl}/translate`, {
        method: 'POST',
        headers,
        body: JSON.stringify({
          q: text,
          source,
          target,
          format
        })
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      return data.translatedText;
    } catch (error) {
      if (error.message.includes('fetch')) {
        throw new Error('Cannot connect to translation server');
      }
      throw error;
    }
  }

  /**
   * Detect the language of the text
   * @param {string} text - Text to detect language for
   * @returns {Promise<{language: string, confidence: number}>}
   */
  async detectLanguage(text) {
    if (!text || !text.trim()) {
      throw new Error('Text cannot be empty');
    }

    const headers = {
      'Content-Type': 'application/json'
    };

    if (this.apiKey) {
      headers['X-API-Key'] = this.apiKey;
    }

    try {
      const response = await fetch(`${this.baseUrl}/detect`, {
        method: 'POST',
        headers,
        body: JSON.stringify({ q: text })
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      if (error.message.includes('fetch')) {
        throw new Error('Cannot connect to translation server');
      }
      throw error;
    }
  }

  /**
   * Get list of supported languages
   * @returns {Promise<Array<{code: string, name: string}>>}
   */
  async getLanguages() {
    const headers = {};

    if (this.apiKey) {
      headers['X-API-Key'] = this.apiKey;
    }

    try {
      const response = await fetch(`${this.baseUrl}/languages`, {
        headers
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      if (error.message.includes('fetch')) {
        throw new Error('Cannot connect to translation server');
      }
      throw error;
    }
  }

  /**
   * Check if the translation server is healthy
   * @returns {Promise<boolean>}
   */
  async healthCheck() {
    try {
      const response = await fetch(`${this.baseUrl}/health`);
      return response.ok;
    } catch (error) {
      return false;
    }
  }

  /**
   * Translate multiple texts in batch
   * @param {Array<string>} texts - Array of texts to translate
   * @param {string} source - Source language code or 'auto'
   * @param {string} target - Target language code
   * @param {number} delay - Delay between requests in ms (default: 100)
   * @returns {Promise<Array<string>>}
   */
  async translateBatch(texts, source = 'auto', target = 'en', delay = 100) {
    const results = [];
    
    for (let i = 0; i < texts.length; i++) {
      try {
        const translated = await this.translate(texts[i], source, target);
        results.push(translated);
        
        // Add delay between requests (except for the last one)
        if (i < texts.length - 1 && delay > 0) {
          await new Promise(resolve => setTimeout(resolve, delay));
        }
      } catch (error) {
        results.push(null); // Add null for failed translations
        console.error(`Translation failed for text ${i + 1}:`, error);
      }
    }
    
    return results;
  }
}

// Export for different environments
if (typeof module !== 'undefined' && module.exports) {
  // Node.js
  module.exports = TranslationClient;
} else if (typeof window !== 'undefined') {
  // Browser
  window.TranslationClient = TranslationClient;
}

// Usage example:
/*
// Option 1: Without API key (if API_KEY_REQUIRED=false)
const client = new TranslationClient('https://translate.shravani.group/');

// Option 2: With API key from environment variable (RECOMMENDED)
// For Next.js: NEXT_PUBLIC_TRANSLATE_API_KEY
// For React: REACT_APP_TRANSLATE_API_KEY
// For Vue: VUE_APP_TRANSLATE_API_KEY
const apiKey = process.env.NEXT_PUBLIC_TRANSLATE_API_KEY || 
               process.env.REACT_APP_TRANSLATE_API_KEY || 
               process.env.VUE_APP_TRANSLATE_API_KEY;

const securedClient = new TranslationClient(
  'https://translate.shravani.group/',
  apiKey  // ← From environment variable, never hardcode!
);

// Translate
securedClient.translate('Hello, world!', 'en', 'es')
  .then(translated => console.log(translated))
  .catch(error => console.error('Error:', error));

// Detect language
securedClient.detectLanguage('Bonjour')
  .then(result => console.log(result))
  .catch(error => console.error('Error:', error));

// Get languages
securedClient.getLanguages()
  .then(languages => console.log(languages))
  .catch(error => console.error('Error:', error));
*/

