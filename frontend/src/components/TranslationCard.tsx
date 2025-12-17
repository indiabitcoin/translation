import { useEffect } from 'react';
import { useTranslation } from '../contexts/TranslationContext';
import { useAuth } from '../contexts/AuthContext';
import { useToast } from '../contexts/ToastContext';

export default function TranslationCard() {
  const {
    languages,
    sourceLanguage,
    targetLanguage,
    sourceText,
    targetText,
    isTranslating,
    setSourceLanguage,
    setTargetLanguage,
    setSourceText,
    translate,
    detectLanguage,
    swapLanguages,
    clearTranslation,
  } = useTranslation();

  const { user, usage, updateUsage } = useAuth();
  const { showToast } = useToast();

  // Auto-translate with debounce
  useEffect(() => {
    if (!sourceText.trim()) return;
    
    const timer = setTimeout(() => {
      translate();
    }, 1000);

    return () => clearTimeout(timer);
  }, [sourceText, sourceLanguage, targetLanguage]);

  const handleTranslate = async () => {
    // Check usage limits
    if (user && usage.used + sourceText.length > usage.limit) {
      showToast('Character limit exceeded. Please upgrade your plan.', 'error');
      return;
    }

    await translate();
    
    if (user) {
      updateUsage(sourceText.length);
    }
  };

  const copyToClipboard = () => {
    if (targetText) {
      navigator.clipboard.writeText(targetText);
      showToast('Translation copied to clipboard!', 'success');
    }
  };

  const speakText = () => {
    if (targetText && 'speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(targetText);
      utterance.lang = targetLanguage;
      window.speechSynthesis.speak(utterance);
    }
  };

  const usagePercentage = user ? (usage.used / usage.limit) * 100 : 0;

  return (
    <section className="translate-section">
      <div className="translation-card">
        <div className="card-header">
          <h2>
            <i className="fas fa-exchange-alt"></i> Translate Text
          </h2>

          {user && (
            <div className="usage-stats">
              <span>
                {usage.used.toLocaleString()} / {usage.limit === Infinity ? '∞' : usage.limit.toLocaleString()} characters
              </span>
              <div className="usage-bar">
                <div
                  className="usage-progress"
                  style={{ width: `${Math.min(usagePercentage, 100)}%` }}
                />
              </div>
            </div>
          )}
        </div>

        <div className="translation-container">
          {/* Source Language */}
          <div className="translation-box">
            <div className="box-header">
              <select
                className="lang-select"
                value={sourceLanguage}
                onChange={(e) => setSourceLanguage(e.target.value)}
              >
                <option value="auto">Auto-detect</option>
                {languages.map((lang) => (
                  <option key={lang.code} value={lang.code}>
                    {lang.name}
                  </option>
                ))}
              </select>

              <button
                className="btn-icon"
                onClick={swapLanguages}
                title="Swap languages"
              >
                <i className="fas fa-exchange-alt"></i>
              </button>

              <button
                className="btn-icon"
                onClick={clearTranslation}
                title="Clear"
              >
                <i className="fas fa-times"></i>
              </button>
            </div>

            <textarea
              className="translation-textarea"
              placeholder="Enter text to translate..."
              rows={8}
              value={sourceText}
              onChange={(e) => setSourceText(e.target.value)}
            />

            <div className="box-footer">
              <span className="char-count">{sourceText.length} characters</span>
              <button className="btn-icon" onClick={detectLanguage}>
                <i className="fas fa-search"></i> Detect Language
              </button>
            </div>
          </div>

          {/* Target Language */}
          <div className="translation-box">
            <div className="box-header">
              <select
                className="lang-select"
                value={targetLanguage}
                onChange={(e) => setTargetLanguage(e.target.value)}
              >
                {languages.map((lang) => (
                  <option key={lang.code} value={lang.code}>
                    {lang.name}
                  </option>
                ))}
              </select>

              <button
                className="btn-icon"
                onClick={copyToClipboard}
                title="Copy translation"
              >
                <i className="fas fa-copy"></i>
              </button>

              <button
                className="btn-icon"
                onClick={() => setSourceText('')}
                title="Clear"
              >
                <i className="fas fa-times"></i>
              </button>
            </div>

            <textarea
              className="translation-textarea"
              placeholder="Translation will appear here..."
              rows={8}
              value={targetText}
              readOnly
            />

            <div className="box-footer">
              <span className="char-count">{targetText.length} characters</span>
              <button className="btn-icon" onClick={speakText} title="Listen">
                <i className="fas fa-volume-up"></i>
              </button>
            </div>
          </div>
        </div>

        <div className="card-footer">
          <button
            className="btn btn-primary btn-large"
            onClick={handleTranslate}
            disabled={isTranslating || !sourceText.trim()}
          >
            {isTranslating ? (
              <>
                <i className="fas fa-spinner fa-spin"></i> Translating...
              </>
            ) : (
              <>
                <i className="fas fa-language"></i> Translate
              </>
            )}
          </button>
        </div>
      </div>
    </section>
  );
}
