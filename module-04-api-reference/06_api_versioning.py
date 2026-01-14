"""
06_api_versioning.py - Handle API versioning and compatibility
"""

versioning_guide = """
API VERSIONING & BACKWARD COMPATIBILITY:

Current API Version: v1
URL: https://api.openai.com/v1/

Stability Commitments:
1. REST API (v1) maintains backward compatibility
2. First-party SDKs follow semantic versioning
3. Model families maintained as stable units

Backward-Compatible Changes:
✅ Adding new API endpoints
✅ Adding optional parameters
✅ Adding new response fields
✅ New event types
✅ Changing property order in JSON

Breaking Changes (will be versioned):
❌ Removing endpoints
❌ Removing required parameters
❌ Removing response fields
❌ Changing parameter types
❌ Changing authentication

Model Versioning:
- Latest: gpt-3.5-turbo (updates automatically)
- Pinned: gpt-3.5-turbo-0125 (static snapshot)

Best Practices:
1. Pin model versions in production:
   model="gpt-3.5-turbo-0125"  # Not "gpt-3.5-turbo"

2. Test before upgrading:
   - Run evals on new versions
   - Compare outputs
   - Check breaking changes

3. Monitor API changelog:
   https://platform.openai.com/docs/changelog

4. Use feature flags:
   - Test new versions with small traffic
   - Rollback if issues

5. Version your prompts:
   - Store prompts with version tags
   - Test compatibility

Example Migration:
# Old (deprecated)
response = openai.Completion.create(...)

# New (current)
response = client.chat.completions.create(...)
"""

print(versioning_guide)
