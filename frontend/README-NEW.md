# LibreTranslate Modern Frontend

A modern, responsive React + TypeScript frontend for LibreTranslate translation service.

## Features

- 🚀 Built with React 18 + TypeScript + Vite
- 🎨 Modern, responsive UI design
- ⚡ Fast development with Vite HMR
- 🔐 User authentication & authorization
- 📊 Usage tracking dashboard
- 💳 Multiple pricing tiers
- 🌍 Support for 100+ languages
- 🎯 Real-time translation with debouncing
- 📱 Mobile-responsive design
- 🔔 Toast notifications
- 🎤 Text-to-speech support
- 📋 Copy to clipboard functionality

## Tech Stack

- **Framework**: React 18
- **Language**: TypeScript
- **Build Tool**: Vite
- **Styling**: Modern CSS with CSS variables
- **Icons**: Font Awesome
- **State Management**: React Context API

## Getting Started

### Prerequisites

- Node.js >= 18.0.0
- npm or yarn

### Installation

1. Install dependencies:
```bash
npm install
```

2. Create environment file:
```bash
cp .env.example .env
```

3. Configure your API URL in `.env`:
```env
VITE_API_URL=http://localhost:5000
```

### Development

Start the development server:
```bash
npm run dev
```

The app will be available at `http://localhost:3000`

### Production Build

Build for production:
```bash
npm run build
```

Preview production build:
```bash
npm run preview
```

### Legacy Server

If you need to use the legacy Express server:
```bash
npm run legacy
```

## Project Structure

```
frontend/
├── src/
│   ├── components/          # React components
│   │   ├── Navbar.tsx
│   │   ├── Hero.tsx
│   │   ├── TranslationCard.tsx
│   │   ├── Pricing.tsx
│   │   ├── Dashboard.tsx
│   │   ├── AuthModal.tsx
│   │   └── Toast.tsx
│   ├── contexts/            # React contexts
│   │   ├── AuthContext.tsx
│   │   ├── TranslationContext.tsx
│   │   └── ToastContext.tsx
│   ├── services/            # API services
│   │   └── api.ts
│   ├── styles/              # CSS styles
│   │   └── index.css
│   ├── types/               # TypeScript types
│   │   └── index.ts
│   ├── App.tsx              # Main app component
│   └── main.tsx             # App entry point
├── index-new.html           # HTML template
├── vite.config.ts           # Vite configuration
├── tsconfig.json            # TypeScript configuration
└── package.json             # Dependencies

```

## API Integration

The frontend communicates with the LibreTranslate backend API:

- `GET /languages` - Get available languages
- `POST /translate` - Translate text
- `POST /detect` - Detect language
- `POST /api/auth/login` - User login (optional)
- `POST /api/auth/signup` - User signup (optional)
- `POST /api/auth/logout` - User logout (optional)

## Features

### Translation
- Auto-detect source language
- Real-time translation with 1-second debounce
- Character count tracking
- Language detection
- Swap languages
- Copy translation to clipboard
- Text-to-speech support

### Authentication (Optional)
- User registration and login
- JWT token-based authentication
- Persistent sessions with localStorage

### Dashboard
- Usage tracking
- Plan management
- Account information
- API key display

### Pricing
- Free tier (10,000 characters/month)
- Pro tier (1,000,000 characters/month)
- Enterprise tier (unlimited)

## Configuration

### Environment Variables

- `VITE_API_URL`: Backend API URL (default: same origin)

### Vite Proxy

The Vite dev server proxies API requests to avoid CORS issues. Configure in `vite.config.ts`:

```typescript
proxy: {
  '/api': {
    target: 'http://localhost:5000',
    changeOrigin: true,
  },
}
```

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - see LICENSE file for details
