export interface Language {
  code: string;
  name: string;
}

export interface TranslationRequest {
  q: string;
  source: string;
  target: string;
  format?: 'text' | 'html';
}

export interface TranslationResponse {
  translatedText: string;
  detectedLanguage?: {
    language: string;
    confidence: number;
  };
}

export interface DetectRequest {
  q: string;
}

export interface DetectResponse {
  language: string;
  confidence: number;
}

export interface User {
  id: string;
  email: string;
  name: string;
  plan: 'free' | 'pro' | 'enterprise';
  apiKey?: string;
}

export interface Usage {
  used: number;
  limit: number;
}

export type ToastType = 'success' | 'error' | 'warning' | 'info';

export interface ToastMessage {
  id: string;
  message: string;
  type: ToastType;
}
