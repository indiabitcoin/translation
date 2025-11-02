/**
 * Real-Time Translation Utilities
 * 
 * Use these functions to translate website content on-the-fly
 */

class RealtimeTranslator {
  constructor(apiUrl, apiKey = null) {
    this.apiUrl = apiUrl;
    this.apiKey = apiKey;
    this.cache = new Map(); // Cache translations
    this.translating = new Set(); // Track ongoing translations
  }

  /**
   * Translate text with caching
   */
  async translate(text, source = 'auto', target = 'en') {
    if (!text || !text.trim()) return text;
    
    // Check cache
    const cacheKey = `${source}-${target}-${text}`;
    if (this.cache.has(cacheKey)) {
      return this.cache.get(cacheKey);
    }

    // Check if already translating this
    if (this.translating.has(cacheKey)) {
      // Wait for ongoing translation
      await new Promise(resolve => {
        const checkInterval = setInterval(() => {
          if (!this.translating.has(cacheKey)) {
            clearInterval(checkInterval);
            resolve();
          }
        }, 50);
      });
      return this.cache.get(cacheKey) || text;
    }

    this.translating.add(cacheKey);

    try {
      const headers = { 'Content-Type': 'application/json' };
      if (this.apiKey) headers['X-API-Key'] = this.apiKey;

      const response = await fetch(`${this.apiUrl}/translate`, {
        method: 'POST',
        headers,
        body: JSON.stringify({ q: text, source, target, format: 'text' })
      });

      if (!response.ok) throw new Error(`HTTP ${response.status}`);

      const data = await response.json();
      const translated = data.translatedText;
      
      // Cache result
      this.cache.set(cacheKey, translated);
      return translated;
    } catch (error) {
      console.error('Translation failed:', error);
      return text; // Return original on error
    } finally {
      this.translating.delete(cacheKey);
    }
  }

  /**
   * Translate a DOM element's text content
   */
  async translateElement(element, targetLang, preserveHtml = false) {
    if (!element) return;

    const originalText = element.textContent.trim();
    if (!originalText) return;

    // Show loading state
    const original = element.innerHTML;
    element.style.opacity = '0.5';
    element.textContent = 'Translating...';

    try {
      const translated = await this.translate(originalText, 'auto', targetLang);
      element.textContent = translated;
      element.setAttribute('data-translated', targetLang);
      element.setAttribute('data-original', originalText);
    } catch (error) {
      element.innerHTML = original; // Restore on error
      console.error('Translation failed:', error);
    } finally {
      element.style.opacity = '1';
    }
  }

  /**
   * Translate all elements with a specific class or selector
   */
  async translateSelector(selector, targetLang) {
    const elements = document.querySelectorAll(selector);
    const translations = [];

    for (const element of elements) {
      if (element.textContent.trim()) {
        translations.push(this.translateElement(element, targetLang));
      }
    }

    await Promise.all(translations);
  }

  /**
   * Translate selected text (right-click or button click)
   */
  async translateSelection(targetLang) {
    const selection = window.getSelection();
    if (!selection || selection.isCollapsed) {
      return null;
    }

    const selectedText = selection.toString().trim();
    if (!selectedText) return null;

    const translated = await this.translate(selectedText, 'auto', targetLang);
    return translated;
  }
}

// Export for different environments
if (typeof module !== 'undefined' && module.exports) {
  module.exports = RealtimeTranslator;
} else if (typeof window !== 'undefined') {
  window.RealtimeTranslator = RealtimeTranslator;
}

