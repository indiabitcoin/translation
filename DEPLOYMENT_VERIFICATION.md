# Deployment Verification Checklist

Use this checklist to verify that the language checking features are properly deployed and working.

## Pre-Deployment Checklist

- [ ] Code pushed to GitHub: `https://github.com/indiabitcoin/translation`
- [ ] All files committed:
  - [ ] `main.py` (with `verify_api_key_optional` function)
  - [ ] `check_api_languages.py`
  - [ ] `check_backend_languages.py`
  - [ ] Documentation files

## Deployment Steps

- [ ] **Step 1**: Deploy updated code to server
  - [ ] If using Coolify: Click "Redeploy" in dashboard
  - [ ] If manual: `git pull origin main` and restart service
  - [ ] Wait for deployment to complete (check logs)

- [ ] **Step 2**: Verify server is running
  ```bash
  curl https://api.shravani.group/health
  ```
  Expected: `{"status":"ok"}`

- [ ] **Step 3**: Test `/languages` endpoint (should work without API key)
  ```bash
  curl https://api.shravani.group/languages
  ```
  Expected: JSON array of language objects
  ❌ If you get `{"detail":"API key required"}` → Deployment not complete

- [ ] **Step 4**: Count languages
  ```bash
  curl https://api.shravani.group/languages | jq 'length'
  ```
  Expected: Number (e.g., 86, 100+, etc.)

- [ ] **Step 5**: Run language check script
  ```bash
  python check_api_languages.py --api-url https://api.shravani.group
  ```
  Expected: Formatted report showing:
  - Total languages
  - Language list grouped by region
  - Package information (if available)

## Verification Tests

### Test 1: Public Access to Languages Endpoint

```bash
# Should work without API key
curl -X GET https://api.shravani.group/languages \
  -H "Accept: application/json"
```

✅ **Success**: Returns JSON array of languages  
❌ **Failure**: Returns `{"detail":"API key required"}`

### Test 2: Language Count

```bash
curl https://api.shravani.group/languages | jq '. | length'
```

✅ **Success**: Returns a number > 0  
❌ **Failure**: Returns 0 or error

### Test 3: Language Check Script

```bash
python check_api_languages.py --api-url https://api.shravani.group
```

✅ **Success**: Shows formatted report with language count  
❌ **Failure**: Shows error message

### Test 4: Package Information (Optional)

```bash
# This may still require API key
curl -H "X-API-Key: YOUR_KEY" https://api.shravani.group/packages
```

✅ **Success**: Returns package information  
ℹ️ **Note**: This endpoint may still require authentication

## Expected Results

### Default Configuration
- **Languages**: ~86 languages
- **Language Pairs**: Hundreds to thousands
- **Response Time**: < 1 second for `/languages` endpoint

### Extended Configuration (INSTALL_ALL_LANGUAGES=true)
- **Languages**: 100+ languages
- **Language Pairs**: Thousands
- **Response Time**: < 2 seconds for `/languages` endpoint

## Troubleshooting

### Issue: Still getting "API key required"

**Check:**
1. Is the deployment complete? Check server logs
2. Is the new code running? Check process/container
3. Did you restart the server after deployment?
4. Wait 2-3 minutes for changes to propagate

**Solution:**
```bash
# Verify code is updated
# Check main.py has verify_api_key_optional function
grep "verify_api_key_optional" main.py

# Restart server
# Coolify: Redeploy
# Manual: Restart service
```

### Issue: Empty language list

**Check:**
1. Are models installed? Check `/packages` endpoint
2. Check server logs for installation errors
3. Verify `UPDATE_MODELS` or `INSTALL_ALL_LANGUAGES` settings

**Solution:**
```bash
# Check packages
curl https://api.shravani.group/packages

# Check server logs for model installation
# Set UPDATE_MODELS=true if needed
```

### Issue: Script can't connect

**Check:**
1. API URL is correct: `https://api.shravani.group`
2. Server is accessible: `curl https://api.shravani.group/health`
3. Network/firewall settings
4. DNS resolution

**Solution:**
```bash
# Test connectivity
ping api.shravani.group

# Test HTTPS
curl -v https://api.shravani.group/health
```

## Quick Verification Commands

Run these commands in sequence:

```bash
# 1. Health check
echo "1. Health check:"
curl -s https://api.shravani.group/health | jq

# 2. Languages endpoint (should work without key)
echo -e "\n2. Languages endpoint:"
curl -s https://api.shravani.group/languages | jq 'length'

# 3. Sample languages
echo -e "\n3. Sample languages:"
curl -s https://api.shravani.group/languages | jq '.[0:5]'

# 4. Full language check
echo -e "\n4. Running full language check:"
python check_api_languages.py --api-url https://api.shravani.group
```

## Success Criteria

✅ All tests pass  
✅ `/languages` endpoint is publicly accessible  
✅ Language check script works without API key  
✅ Language count matches expected range (86+ languages)  
✅ Documentation is accessible  

## Post-Deployment

After successful deployment:

1. **Document actual language count** in your notes
2. **Share results** with your team
3. **Update frontend** if language count changed significantly
4. **Monitor usage** of the `/languages` endpoint
5. **Consider caching** if endpoint gets heavy traffic

## Next Actions

Once verified:
- [ ] Update frontend to reflect actual language count
- [ ] Add language statistics to dashboard
- [ ] Monitor API usage and performance
- [ ] Consider adding language popularity metrics

---

**Last Updated**: After deployment  
**Status**: Ready for verification  
**Priority**: High

