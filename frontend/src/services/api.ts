import type { 
  Language, 
  TranslationRequest, 
  TranslationResponse, 
  DetectRequest, 
  DetectResponse 
} from '../types';

// Use explicit API base URL from env for direct frontend calls.
// No BFF/proxy used in production; backend must handle CORS.
const API_BASE_URL: string = (import.meta.env.VITE_API_URL as string) || 'https://api.shravani.group';

class ApiService {
  private baseUrl: string;
  private apiKey?: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  setApiKey(apiKey?: string) {
    this.apiKey = apiKey;
  }

  private async fetchWithAuth(url: string, options: RequestInit = {}) {
    const headers = new Headers({ 'Content-Type': 'application/json' });

    // Merge any provided headers
    if (options.headers) {
      const incoming = options.headers as HeadersInit;
      if (incoming instanceof Headers) {
        incoming.forEach((value, key) => headers.set(key, value));
      } else if (Array.isArray(incoming)) {
        for (const [key, value] of incoming) headers.set(key, value);
      } else {
        Object.entries(incoming as Record<string, string>).forEach(([k, v]) =>
          headers.set(k, v)
        );
      }
    }

    if (this.apiKey) {
      headers.set('X-API-Key', this.apiKey);
    }

    const response = await fetch(`${this.baseUrl}${url}`, {
      ...options,
      headers,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ error: 'Request failed' }));
      throw new Error(error.error || error.detail || 'Request failed');
    }

    return response.json();
  }

  async getLanguages(): Promise<Language[]> {
    return this.fetchWithAuth('/languages');
  }

  async translate(request: TranslationRequest): Promise<TranslationResponse> {
    return this.fetchWithAuth('/translate', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  async detect(request: DetectRequest): Promise<DetectResponse[]> {
    return this.fetchWithAuth('/detect', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  // Auth endpoints (if your backend supports them)
  async login(email: string, password: string) {
    return this.fetchWithAuth('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
  }

  async signup(name: string, email: string, password: string) {
    return this.fetchWithAuth('/api/auth/signup', {
      method: 'POST',
      body: JSON.stringify({ name, email, password }),
    });
  }

  async logout() {
    return this.fetchWithAuth('/api/auth/logout', {
      method: 'POST',
    });
  }
}

export const apiService = new ApiService();
