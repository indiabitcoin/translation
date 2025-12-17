// Application State
// API Server URL - Update this to match your backend server
const API_BASE_URL = window.location.hostname === 'translate.shravani.group' 
    ? 'https://api.shravani.group'  // Production: separate API server
    : window.location.origin;  // Development: same server

const AppState = {
    user: null,
    plan: 'free',
    usage: {
        used: 0,
        limit: 10000
    },
    languages: [],
    apiUrl: API_BASE_URL
};

// Initialize App
document.addEventListener('DOMContentLoaded', () => {
    init();
});

async function init() {
    await loadLanguages();
    setupEventListeners();
    checkAuth();
    updateUI();
}

// Load Languages
async function loadLanguages() {
    try {
        const response = await fetch(`${AppState.apiUrl}/languages`);
        if (response.ok) {
            const languages = await response.json();
            AppState.languages = languages;
            populateLanguageSelects();
        }
    } catch (error) {
        console.error('Failed to load languages:', error);
        showToast('Failed to load languages', 'error');
    }
}

function populateLanguageSelects() {
    const sourceSelect = document.getElementById('source-lang');
    const targetSelect = document.getElementById('target-lang');
    
    // Add languages to selects
    AppState.languages.forEach(lang => {
        const sourceOption = document.createElement('option');
        sourceOption.value = lang.code;
        sourceOption.textContent = lang.name;
        sourceSelect.appendChild(sourceOption);
        
        const targetOption = document.createElement('option');
        targetOption.value = lang.code;
        targetOption.textContent = lang.name;
        targetSelect.appendChild(targetOption);
    });
    
    // Set default target to Spanish
    targetSelect.value = 'es';
}

// Event Listeners
function setupEventListeners() {
    // Navigation
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const section = link.getAttribute('href').substring(1);
            showSection(section);
        });
    });
    
    // Translation
    document.getElementById('translate-btn').addEventListener('click', handleTranslate);
    document.getElementById('swap-btn').addEventListener('click', swapLanguages);
    document.getElementById('detect-btn').addEventListener('click', detectLanguage);
    document.getElementById('copy-btn').addEventListener('click', copyTranslation);
    document.getElementById('speak-btn').addEventListener('click', speakTranslation);
    document.getElementById('clear-source').addEventListener('click', () => {
        document.getElementById('source-text').value = '';
        updateCharCount();
    });
    document.getElementById('clear-target').addEventListener('click', () => {
        document.getElementById('target-text').value = '';
    });
    
    // Character count
    document.getElementById('source-text').addEventListener('input', updateCharCount);
    
    // Auto-translate on change (debounced)
    let translateTimeout;
    document.getElementById('source-text').addEventListener('input', () => {
        clearTimeout(translateTimeout);
        translateTimeout = setTimeout(() => {
            if (document.getElementById('source-text').value.trim() && 
                document.getElementById('target-lang').value) {
                handleTranslate();
            }
        }, 1000);
    });
    
    // Modals
    document.getElementById('login-btn').addEventListener('click', () => showModal('login-modal'));
    document.getElementById('signup-btn').addEventListener('click', () => showModal('signup-modal'));
    document.getElementById('close-login').addEventListener('click', () => hideModal('login-modal'));
    document.getElementById('close-signup').addEventListener('click', () => hideModal('signup-modal'));
    document.getElementById('switch-to-signup').addEventListener('click', (e) => {
        e.preventDefault();
        hideModal('login-modal');
        showModal('signup-modal');
    });
    document.getElementById('switch-to-login').addEventListener('click', (e) => {
        e.preventDefault();
        hideModal('signup-modal');
        showModal('login-modal');
    });
    
    // Forms
    document.getElementById('login-form').addEventListener('submit', handleLogin);
    document.getElementById('signup-form').addEventListener('submit', handleSignup);
    document.getElementById('logout-btn').addEventListener('click', handleLogout);
    
    // Pricing
    document.getElementById('pro-plan-btn').addEventListener('click', () => upgradePlan('pro'));
    document.getElementById('enterprise-plan-btn').addEventListener('click', () => upgradePlan('enterprise'));
    document.getElementById('upgrade-btn-dashboard').addEventListener('click', () => {
        showSection('pricing');
    });
    
    // User menu
    document.getElementById('user-btn').addEventListener('click', (e) => {
        e.stopPropagation();
        const dropdown = document.getElementById('user-dropdown');
        dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
    });
    
    // Close dropdown on outside click
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.user-menu')) {
            document.getElementById('user-dropdown').style.display = 'none';
        }
    });
}

// Translation Functions
async function handleTranslate() {
    const sourceText = document.getElementById('source-text').value.trim();
    const sourceLang = document.getElementById('source-lang').value;
    const targetLang = document.getElementById('target-lang').value;
    
    if (!sourceText) {
        showToast('Please enter text to translate', 'warning');
        return;
    }
    
    if (!targetLang) {
        showToast('Please select a target language', 'warning');
        return;
    }
    
    // Check usage limit
    if (AppState.user && AppState.usage.used + sourceText.length > AppState.usage.limit) {
        showToast('Character limit exceeded. Please upgrade your plan.', 'error');
        showSection('pricing');
        return;
    }
    
    const loadingSpinner = document.getElementById('loading-spinner');
    const translateBtn = document.getElementById('translate-btn');
    
    loadingSpinner.style.display = 'flex';
    translateBtn.disabled = true;
    
    try {
        const response = await fetch(`${AppState.apiUrl}/translate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                ...(AppState.user?.apiKey && { 'X-API-Key': AppState.user.apiKey })
            },
            body: JSON.stringify({
                q: sourceText,
                source: sourceLang === 'auto' ? 'auto' : sourceLang,
                target: targetLang,
                format: 'text'
            })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Translation failed');
        }
        
        const data = await response.json();
        document.getElementById('target-text').value = data.translatedText;
        
        // Update usage
        if (AppState.user) {
            AppState.usage.used += sourceText.length;
            updateUsageDisplay();
            await saveUsage();
        }
        
        showToast('Translation successful!', 'success');
    } catch (error) {
        console.error('Translation error:', error);
        showToast(error.message || 'Translation failed', 'error');
    } finally {
        loadingSpinner.style.display = 'none';
        translateBtn.disabled = false;
    }
}

function swapLanguages() {
    const sourceLang = document.getElementById('source-lang').value;
    const targetLang = document.getElementById('target-lang').value;
    const sourceText = document.getElementById('source-text').value;
    const targetText = document.getElementById('target-text').value;
    
    document.getElementById('source-lang').value = targetLang;
    document.getElementById('target-lang').value = sourceLang;
    document.getElementById('source-text').value = targetText;
    document.getElementById('target-text').value = sourceText;
    
    updateCharCount();
}

async function detectLanguage() {
    const sourceText = document.getElementById('source-text').value.trim();
    
    if (!sourceText) {
        showToast('Please enter text to detect', 'warning');
        return;
    }
    
    try {
        const response = await fetch(`${AppState.apiUrl}/detect`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                ...(AppState.user?.apiKey && { 'X-API-Key': AppState.user.apiKey })
            },
            body: JSON.stringify({ q: sourceText })
        });
        
        if (response.ok) {
            const data = await response.json();
            document.getElementById('source-lang').value = data.language;
            showToast(`Detected language: ${data.language} (${(data.confidence * 100).toFixed(1)}% confidence)`, 'success');
        }
    } catch (error) {
        console.error('Detection error:', error);
        showToast('Language detection failed', 'error');
    }
}

function copyTranslation() {
    const targetText = document.getElementById('target-text').value;
    if (targetText) {
        navigator.clipboard.writeText(targetText);
        showToast('Translation copied to clipboard!', 'success');
    }
}

function speakTranslation() {
    const targetText = document.getElementById('target-text').value;
    const targetLang = document.getElementById('target-lang').value;
    
    if (targetText && 'speechSynthesis' in window) {
        const utterance = new SpeechSynthesisUtterance(targetText);
        utterance.lang = targetLang;
        window.speechSynthesis.speak(utterance);
    }
}

function updateCharCount() {
    const sourceText = document.getElementById('source-text').value;
    const count = sourceText.length;
    document.getElementById('source-char-count').textContent = `${count} characters`;
    document.getElementById('target-char-count').textContent = `${document.getElementById('target-text').value.length} characters`;
}

// Authentication
async function handleLogin(e) {
    e.preventDefault();
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;
    
    try {
        const response = await fetch(`${AppState.apiUrl}/api/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });
        
        if (response.ok) {
            const data = await response.json();
            AppState.user = data.user;
            AppState.plan = data.user.plan;
            AppState.usage = data.usage;
            localStorage.setItem('authToken', data.token);
            localStorage.setItem('user', JSON.stringify(data.user));
            hideModal('login-modal');
            updateUI();
            showToast('Login successful!', 'success');
        } else {
            const error = await response.json();
            throw new Error(error.detail || 'Login failed');
        }
    } catch (error) {
        showToast(error.message || 'Login failed', 'error');
    }
}

async function handleSignup(e) {
    e.preventDefault();
    const name = document.getElementById('signup-name').value;
    const email = document.getElementById('signup-email').value;
    const password = document.getElementById('signup-password').value;
    
    try {
        const response = await fetch(`${AppState.apiUrl}/api/auth/signup`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, email, password })
        });
        
        if (response.ok) {
            const data = await response.json();
            AppState.user = data.user;
            AppState.plan = 'free';
            AppState.usage = { used: 0, limit: 10000 };
            localStorage.setItem('authToken', data.token);
            localStorage.setItem('user', JSON.stringify(data.user));
            hideModal('signup-modal');
            updateUI();
            showToast('Account created successfully!', 'success');
        } else {
            const error = await response.json();
            throw new Error(error.detail || 'Signup failed');
        }
    } catch (error) {
        showToast(error.message || 'Signup failed', 'error');
    }
}

function handleLogout() {
    AppState.user = null;
    AppState.plan = 'free';
    AppState.usage = { used: 0, limit: 10000 };
    localStorage.removeItem('authToken');
    localStorage.removeItem('user');
    updateUI();
    showToast('Logged out successfully', 'success');
}

function checkAuth() {
    const token = localStorage.getItem('authToken');
    const userStr = localStorage.getItem('user');
    
    if (token && userStr) {
        try {
            AppState.user = JSON.parse(userStr);
            AppState.plan = AppState.user.plan || 'free';
            loadUserUsage();
        } catch (error) {
            console.error('Failed to parse user data:', error);
        }
    }
}

async function loadUserUsage() {
    if (!AppState.user) return;
    
    try {
        const response = await fetch(`${AppState.apiUrl}/api/user/usage`, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('authToken')}`
            }
        });
        
        if (response.ok) {
            const data = await response.json();
            AppState.usage = data;
        }
    } catch (error) {
        console.error('Failed to load usage:', error);
    }
}

async function saveUsage() {
    if (!AppState.user) return;
    
    try {
        await fetch(`${AppState.apiUrl}/api/user/usage`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('authToken')}`
            },
            body: JSON.stringify({ used: AppState.usage.used })
        });
    } catch (error) {
        console.error('Failed to save usage:', error);
    }
}

// Plan Management
async function upgradePlan(plan) {
    if (!AppState.user) {
        showToast('Please sign in to upgrade', 'warning');
        showModal('login-modal');
        return;
    }
    
    try {
        const response = await fetch(`${AppState.apiUrl}/api/subscription/upgrade`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('authToken')}`
            },
            body: JSON.stringify({ plan })
        });
        
        if (response.ok) {
            const data = await response.json();
            AppState.plan = plan;
            AppState.usage.limit = data.usageLimit;
            AppState.user.plan = plan;
            localStorage.setItem('user', JSON.stringify(AppState.user));
            updateUI();
            showToast(`Upgraded to ${plan} plan!`, 'success');
        } else {
            const error = await response.json();
            throw new Error(error.detail || 'Upgrade failed');
        }
    } catch (error) {
        showToast(error.message || 'Upgrade failed', 'error');
    }
}

// UI Updates
function updateUI() {
    const isAuthenticated = !!AppState.user;
    
    // Navigation
    document.getElementById('login-btn').style.display = isAuthenticated ? 'none' : 'inline-flex';
    document.getElementById('signup-btn').style.display = isAuthenticated ? 'none' : 'inline-flex';
    document.getElementById('user-menu').style.display = isAuthenticated ? 'block' : 'none';
    document.getElementById('dashboard-link').style.display = isAuthenticated ? 'inline-block' : 'none';
    
    if (isAuthenticated) {
        document.getElementById('user-email').textContent = AppState.user.email;
    }
    
    // Plan badge
    const planBadge = document.getElementById('plan-badge');
    if (isAuthenticated) {
        planBadge.style.display = 'inline-flex';
        document.getElementById('plan-name').textContent = 
            AppState.plan.charAt(0).toUpperCase() + AppState.plan.slice(1) + ' Plan';
    } else {
        planBadge.style.display = 'none';
    }
    
    // Usage stats
    const usageStats = document.getElementById('usage-stats');
    if (isAuthenticated) {
        usageStats.style.display = 'block';
        updateUsageDisplay();
    } else {
        usageStats.style.display = 'none';
    }
    
    // Update plan limits
    updatePlanLimits();
}

function updateUsageDisplay() {
    const percentage = (AppState.usage.used / AppState.usage.limit) * 100;
    document.getElementById('usage-text').textContent = 
        `${AppState.usage.used.toLocaleString()} / ${AppState.usage.limit.toLocaleString()} characters`;
    document.getElementById('usage-progress').style.width = `${Math.min(percentage, 100)}%`;
    document.getElementById('usage-progress-large').style.width = `${Math.min(percentage, 100)}%`;
    document.getElementById('usage-value').textContent = AppState.usage.used.toLocaleString();
    document.getElementById('usage-limit').textContent = `of ${AppState.usage.limit.toLocaleString()} characters`;
    document.getElementById('current-plan-display').textContent = 
        AppState.plan.charAt(0).toUpperCase() + AppState.plan.slice(1);
}

function updatePlanLimits() {
    const limits = {
        free: 10000,
        pro: 1000000,
        enterprise: Infinity
    };
    
    AppState.usage.limit = limits[AppState.plan] || limits.free;
    updateUsageDisplay();
}

function showSection(section) {
    // Hide all sections
    document.querySelectorAll('section[id$="-section"]').forEach(s => {
        s.style.display = 'none';
    });
    
    // Show selected section
    const targetSection = document.getElementById(`${section}-section`);
    if (targetSection) {
        targetSection.style.display = 'block';
    }
    
    // Update nav links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${section}`) {
            link.classList.add('active');
        }
    });
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Modal Functions
function showModal(modalId) {
    document.getElementById(modalId).classList.add('show');
}

function hideModal(modalId) {
    document.getElementById(modalId).classList.remove('show');
}

// Toast Notifications
function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'exclamation-triangle'}"></i>
        <span>${message}</span>
    `;
    
    document.getElementById('toast-container').appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'slideIn 0.3s ease-out reverse';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

