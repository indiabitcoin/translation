#!/usr/bin/env node
/**
 * Simple Express server to serve frontend files
 * Useful for development or if you don't have Nginx/Apache
 * 
 * Usage:
 *   npm install express
 *   node server.js
 * 
 * Or with PM2:
 *   pm2 start server.js --name translate-frontend
 */

const express = require('express');
const path = require('path');
const app = express();

const PORT = process.env.PORT || 3000;
const FRONTEND_DIR = path.join(__dirname);

// Security headers
app.use((req, res, next) => {
    res.setHeader('X-Frame-Options', 'SAMEORIGIN');
    res.setHeader('X-Content-Type-Options', 'nosniff');
    res.setHeader('X-XSS-Protection', '1; mode=block');
    res.setHeader('Referrer-Policy', 'strict-origin-when-cross-origin');
    next();
});

// Serve static files
app.use(express.static(FRONTEND_DIR, {
    maxAge: '1y',
    etag: true,
    lastModified: true
}));

// Serve index.html for all routes (SPA routing)
app.get('*', (req, res) => {
    res.sendFile(path.join(FRONTEND_DIR, 'index.html'));
});

// Health check
app.get('/health', (req, res) => {
    res.status(200).send('healthy');
});

app.listen(PORT, () => {
    console.log(`Frontend server running on port ${PORT}`);
    console.log(`Open http://localhost:${PORT} in your browser`);
    console.log(`Frontend directory: ${FRONTEND_DIR}`);
});

