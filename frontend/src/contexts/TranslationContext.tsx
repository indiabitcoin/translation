import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import type { Language } from '../types';
import { apiService } from '../services/api';
import { useToast } from './ToastContext';

interface TranslationContextType {
  languages: Language[];
  sourceLanguage: string;
  targetLanguage: string;
  sourceText: string;
  targetText: string;
  isTranslating: boolean;
  setSourceLanguage: (lang: string) => void;
  setTargetLanguage: (lang: string) => void;
  setSourceText: (text: string) => void;
  setTargetText: (text: string) => void;
  translate: () => Promise<void>;
  detectLanguage: () => Promise<void>;
  swapLanguages: () => void;
  clearTranslation: () => void;
}

const TranslationContext = createContext<TranslationContextType | undefined>(undefined);

export function TranslationProvider({ children }: { children: ReactNode }) {
  const [languages, setLanguages] = useState<Language[]>([]);
  const [sourceLanguage, setSourceLanguage] = useState('auto');
  const [targetLanguage, setTargetLanguage] = useState('es');
  const [sourceText, setSourceText] = useState('');
  const [targetText, setTargetText] = useState('');
  const [isTranslating, setIsTranslating] = useState(false);
  const { showToast } = useToast();

  useEffect(() => {
    loadLanguages();
  }, []);

  const loadLanguages = async () => {
    try {
      const langs = await apiService.getLanguages();
      setLanguages(langs);
    } catch (error) {
      showToast('Failed to load languages', 'error');
      console.error('Failed to load languages:', error);
    }
  };

  const translate = async () => {
    if (!sourceText.trim()) {
      showToast('Please enter text to translate', 'warning');
      return;
    }

    if (!targetLanguage) {
      showToast('Please select a target language', 'warning');
      return;
    }

    setIsTranslating(true);
    try {
      const result = await apiService.translate({
        q: sourceText,
        source: sourceLanguage === 'auto' ? 'auto' : sourceLanguage,
        target: targetLanguage,
        format: 'text',
      });

      setTargetText(result.translatedText);
      showToast('Translation successful!', 'success');
    } catch (error: any) {
      showToast(error.message || 'Translation failed', 'error');
      console.error('Translation error:', error);
    } finally {
      setIsTranslating(false);
    }
  };

  const detectLanguage = async () => {
    if (!sourceText.trim()) {
      showToast('Please enter text to detect', 'warning');
      return;
    }

    try {
      const results = await apiService.detect({ q: sourceText });
      if (results && results.length > 0) {
        const detected = results[0];
        setSourceLanguage(detected.language);
        showToast(
          `Detected: ${detected.language} (${(detected.confidence * 100).toFixed(1)}% confidence)`,
          'success'
        );
      }
    } catch (error: any) {
      showToast(error.message || 'Language detection failed', 'error');
      console.error('Detection error:', error);
    }
  };

  const swapLanguages = () => {
    if (sourceLanguage === 'auto') {
      showToast('Cannot swap with auto-detect', 'warning');
      return;
    }

    setSourceLanguage(targetLanguage);
    setTargetLanguage(sourceLanguage);
    setSourceText(targetText);
    setTargetText(sourceText);
  };

  const clearTranslation = () => {
    setSourceText('');
    setTargetText('');
  };

  return (
    <TranslationContext.Provider
      value={{
        languages,
        sourceLanguage,
        targetLanguage,
        sourceText,
        targetText,
        isTranslating,
        setSourceLanguage,
        setTargetLanguage,
        setSourceText,
        setTargetText,
        translate,
        detectLanguage,
        swapLanguages,
        clearTranslation,
      }}
    >
      {children}
    </TranslationContext.Provider>
  );
}

export function useTranslation() {
  const context = useContext(TranslationContext);
  if (!context) {
    throw new Error('useTranslation must be used within TranslationProvider');
  }
  return context;
}
