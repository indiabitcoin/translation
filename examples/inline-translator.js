/**
 * Inline Translation Script
 * 
 * Add this script to any website to enable "translate on hover/click" functionality
 * 
 * Usage:
 * 1. Include this script in your HTML
 * 2. Add data-translate="true" to any element you want to translate
 * 3. Or use the class "translate-on-click"
 */

(function() {
    'use strict';

    // CONFIGURATION
    const CONFIG = {
        API_URL: 'http://localhost:5000', // Change to your server URL
        API_KEY: null, // Optional API key
        DEFAULT_TARGET: 'es', // Default target language
        SHOW_TOOLTIP: true, // Show translation tooltip
        CACHE_ENABLED: true // Enable caching
    };

    // Translation cache
    const cache = new Map();
    const translatingElements = new WeakMap();

    // Load available languages
    let availableLanguages = [];

    async function loadLanguages() {
        try {
            const response = await fetch(`${CONFIG.API_URL}/languages`);
            availableLanguages = await response.json();
        } catch (error) {
            console.error('Failed to load languages:', error);
        }
    }

    // Translate text
    async function translateText(text, targetLang = CONFIG.DEFAULT_TARGET) {
        if (!text || !text.trim()) return text;

        const cacheKey = `auto-${targetLang}-${text}`;
        if (CONFIG.CACHE_ENABLED && cache.has(cacheKey)) {
            return cache.get(cacheKey);
        }

        try {
            const headers = { 'Content-Type': 'application/json' };
            if (CONFIG.API_KEY) headers['X-API-Key'] = CONFIG.API_KEY;

            const response = await fetch(`${CONFIG.API_URL}/translate`, {
                method: 'POST',
                headers,
                body: JSON.stringify({
                    q: text,
                    source: 'auto',
                    target: targetLang,
                    format: 'text'
                })
            });

            if (!response.ok) throw new Error(`HTTP ${response.status}`);

            const data = await response.json();
            const translated = data.translatedText;

            if (CONFIG.CACHE_ENABLED) {
                cache.set(cacheKey, translated);
            }

            return translated;
        } catch (error) {
            console.error('Translation failed:', error);
            return text;
        }
    }

    // Create translation tooltip
    function createTooltip(element, translatedText) {
        // Remove existing tooltip
        const existing = element.querySelector('.translation-tooltip');
        if (existing) existing.remove();

        const tooltip = document.createElement('div');
        tooltip.className = 'translation-tooltip';
        tooltip.textContent = translatedText;
        tooltip.style.cssText = `
            position: absolute;
            background: #333;
            color: white;
            padding: 8px 12px;
            border-radius: 4px;
            font-size: 14px;
            z-index: 10000;
            max-width: 300px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            pointer-events: none;
            white-space: normal;
            word-wrap: break-word;
        `;

        // Position tooltip
        const rect = element.getBoundingClientRect();
        tooltip.style.top = `${rect.bottom + 5}px`;
        tooltip.style.left = `${rect.left}px`;

        element.style.position = 'relative';
        element.appendChild(tooltip);

        // Auto-hide after 5 seconds
        setTimeout(() => {
            tooltip.remove();
        }, 5000);
    }

    // Translate element on click
    async function translateOnClick(element, targetLang = CONFIG.DEFAULT_TARGET) {
        if (translatingElements.has(element)) return; // Already translating

        const originalText = element.textContent.trim();
        if (!originalText || originalText.length > 500) return; // Skip empty or too long text

        // Mark as translating
        const promise = translateText(originalText, targetLang);
        translatingElements.set(element, promise);

        // Show loading state
        const originalContent = element.innerHTML;
        element.style.opacity = '0.6';
        element.setAttribute('data-translating', 'true');

        try {
            const translated = await promise;

            // Replace content
            element.innerHTML = translated;
            element.setAttribute('data-translated', targetLang);
            element.setAttribute('data-original-text', originalText);
            element.style.opacity = '1';

            if (CONFIG.SHOW_TOOLTIP) {
                createTooltip(element, `✓ Translated to ${targetLang.toUpperCase()}`);
            }
        } catch (error) {
            element.innerHTML = originalContent; // Restore on error
            element.style.opacity = '1';
        } finally {
            translatingElements.delete(element);
            element.removeAttribute('data-translating');
        }
    }

    // Translate on hover (show tooltip with translation)
    async function translateOnHover(element, targetLang = CONFIG.DEFAULT_TARGET) {
        const originalText = element.textContent.trim();
        if (!originalText || originalText.length > 100) return; // Skip long text

        try {
            const translated = await translateText(originalText, targetLang);
            createTooltip(element, translated);
        } catch (error) {
            console.error('Hover translation failed:', error);
        }
    }

    // Restore original text
    function restoreOriginal(element) {
        const original = element.getAttribute('data-original-text');
        if (original) {
            element.textContent = original;
            element.removeAttribute('data-translated');
            element.removeAttribute('data-original-text');
        }
    }

    // Initialize
    function init() {
        loadLanguages();

        // Handle elements with data-translate attribute
        document.querySelectorAll('[data-translate="true"]').forEach(el => {
            el.style.cursor = 'pointer';
            el.addEventListener('click', () => {
                if (el.hasAttribute('data-translated')) {
                    restoreOriginal(el);
                } else {
                    translateOnClick(el);
                }
            });
        });

        // Handle elements with translate-on-click class
        document.querySelectorAll('.translate-on-click').forEach(el => {
            el.style.cursor = 'pointer';
            el.title = 'Click to translate';
            el.addEventListener('click', () => {
                if (el.hasAttribute('data-translated')) {
                    restoreOriginal(el);
                } else {
                    translateOnClick(el);
                }
            });
        });

        // Handle elements with translate-on-hover class
        document.querySelectorAll('.translate-on-hover').forEach(el => {
            el.addEventListener('mouseenter', () => {
                translateOnHover(el);
            });
        });

        // Add right-click context menu option (if supported)
        document.addEventListener('contextmenu', (e) => {
            if (e.target.hasAttribute('data-translate') || 
                e.target.classList.contains('translate-on-click')) {
                // Could show custom context menu here
            }
        });
    }

    // Wait for DOM to be ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // Export for manual use
    window.InlineTranslator = {
        translate: translateText,
        translateElement: translateOnClick,
        setLanguage: (lang) => { CONFIG.DEFAULT_TARGET = lang; },
        setApiUrl: (url) => { CONFIG.API_URL = url; }
    };
})();

