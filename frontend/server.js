#!/usr/bin/env node
/**
 * Production Express server (BFF) to serve the SPA and securely proxy API calls.
 * - Serves built assets from ./dist
 * - Proxies /languages, /translate, /detect to the upstream API server
 * - Strips client X-API-Key and injects server-side key if provided
 * - Adds security headers, rate limits, and body size limits
 *
 * Env vars:
 *   PORT=3000
 *   API_BASE=https://api.shravani.group
 *   UPSTREAM_API_KEY=<optional_server_side_key>
 */

const path = require('path');
const express = require('express');
const helmet = require('helmet');
const morgan = require('morgan');
const rateLimit = require('express-rate-limit');
const { createProxyMiddleware } = require('http-proxy-middleware');

const app = express();

const PORT = process.env.PORT || 3000;
const DIST_DIR = path.join(__dirname, 'dist');
const API_BASE = process.env.API_BASE || 'https://api.shravani.group';
const UPSTREAM_API_KEY = process.env.UPSTREAM_API_KEY || '';

// Trust proxy if behind a reverse proxy (optional)
if (process.env.TRUST_PROXY) {
    app.set('trust proxy', 1);
}

// Security headers via helmet
app.use(helmet({
    contentSecurityPolicy: false, // SPA; consider enabling with proper directives later
    crossOriginEmbedderPolicy: false,
}));

// Additional basic security headers
app.use((req, res, next) => {
    res.setHeader('Referrer-Policy', 'strict-origin-when-cross-origin');
    next();
});

// Logging
app.use(morgan('combined'));

// Body parser with limits
app.use(express.json({ limit: '256kb' }));

// Rate limiting (per IP). Tune as needed.
const commonLimiter = rateLimit({
    windowMs: 60 * 1000, // 1 minute
    max: 60,             // 60 req/min/IP
    standardHeaders: true,
    legacyHeaders: false,
});
app.use(['/languages', '/translate', '/detect'], commonLimiter);

// Helper: build proxy options with server-side API key injection
const apiProxy = createProxyMiddleware({
    target: API_BASE,
    changeOrigin: true,
    xfwd: true,
    onProxyReq: (proxyReq, req, res) => {
        // Strip any client-provided X-API-Key
        proxyReq.removeHeader?.('X-API-Key');
        // Inject server-side API key if configured
        if (UPSTREAM_API_KEY) {
            proxyReq.setHeader('X-API-Key', UPSTREAM_API_KEY);
        }
        // Enforce JSON
        if (req.method === 'POST') {
            proxyReq.setHeader('Content-Type', 'application/json');
        }
    },
});

// Method-restricted routes
app.get('/languages', apiProxy);
app.post('/translate', apiProxy);
app.post('/detect', apiProxy);

// Health check
app.get('/health', (_req, res) => res.status(200).send('healthy'));

// Serve static SPA
app.use(express.static(DIST_DIR, { maxAge: '1y', etag: true }));

// SPA fallback
app.get('*', (_req, res) => {
    res.sendFile(path.join(DIST_DIR, 'index.html'));
});

app.listen(PORT, () => {
    console.log(`Frontend+BFF server running on http://localhost:${PORT}`);
    console.log(`Serving SPA from: ${DIST_DIR}`);
    console.log(`Proxying API to: ${API_BASE}`);
});

