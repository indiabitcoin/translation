# Quick Start - Language Checking

## 🚀 Quick Deployment

1. **Deploy to server** (Coolify: Click "Redeploy")
2. **Test endpoint**: `curl https://api.shravani.group/languages`
3. **Run script**: `python check_api_languages.py`

## 📋 One-Liner Tests

```bash
# Health check
curl https://api.shravani.group/health

# Count languages
curl https://api.shravani.group/languages | jq 'length'

# Full check
python check_api_languages.py --api-url https://api.shravani.group
```

## ✅ Success Indicators

- ✅ `/languages` returns JSON without API key
- ✅ Language count > 0
- ✅ Script shows formatted report

## 📚 Full Documentation

- **Deployment**: `NEXT_STEPS.md`
- **Verification**: `DEPLOYMENT_VERIFICATION.md`
- **Usage**: `CHECK_LANGUAGES_GUIDE.md`
- **Languages**: `LANGUAGE_SUPPORT_SUMMARY.md`

