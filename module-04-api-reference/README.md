# Module 4: API Reference and Authentication

## 📋 Module Overview

**Duration**: 2 hours
**Level**: Intermediate
**Prerequisites**: Modules 1-3 completed

Master API authentication, rate limiting, debugging, and ensure your applications follow best practices for security and reliability.

---

## 🎯 Learning Objectives

- ✅ Master API authentication methods
- ✅ Understand and handle rate limiting
- ✅ Implement request debugging and monitoring
- ✅ Manage multi-organization/project access
- ✅ Use custom request IDs for tracking
- ✅ Handle API versioning and backward compatibility

---

## 📖 Table of Contents

1. [Authentication Deep Dive](#1-authentication-deep-dive)
2. [Rate Limiting](#2-rate-limiting)
3. [Request Debugging](#3-request-debugging)
4. [Multi-Organization Access](#4-multi-organization-access)
5. [API Versioning](#5-api-versioning)
6. [Best Practices](#6-best-practices)

---

## 1. Authentication Deep Dive

### 1.1 API Key Types

```python
"""
01_authentication.py - Comprehensive authentication patterns
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


# Method 1: Environment variable (Recommended)
client = OpenAI()  # Automatically reads OPENAI_API_KEY


# Method 2: Explicit API key
client_explicit = OpenAI(api_key="sk-proj-your-key-here")


# Method 3: Organization and Project specific
client_org = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    organization=os.getenv("OPENAI_ORG_ID"),  # Optional
    project=os.getenv("OPENAI_PROJECT_ID")     # Optional
)


def test_authentication():
    """Test API authentication"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=10
        )
        print("✅ Authentication successful")
        return True
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        return False


if __name__ == "__main__":
    test_authentication()
```

### 1.2 Security Best Practices

```python
"""
02_api_key_security.py - API key security patterns
"""

import os
from dotenv import load_dotenv
from pathlib import Path


class SecureAPIKeyManager:
    """Secure API key management"""

    def __init__(self):
        self.api_key = None
        self._load_key()

    def _load_key(self):
        """Load API key securely"""
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")

        if not self.api_key:
            raise ValueError("API key not found in environment")

    def get_masked_key(self):
        """Return masked version for logging"""
        if self.api_key and len(self.api_key) > 12:
            return f"{self.api_key[:8]}...{self.api_key[-4:]}"
        return "***"

    def validate_key_format(self):
        """Validate key format"""
        if not self.api_key:
            return False

        # OpenAI keys start with 'sk-'
        if not self.api_key.startswith("sk-"):
            print("⚠️  Warning: Key doesn't follow expected format")
            return False

        return True


# Security Checklist
security_checklist = """
API KEY SECURITY CHECKLIST:

✅ DO:
- Store keys in environment variables
- Use .env files (add to .gitignore)
- Rotate keys regularly
- Use different keys for dev/staging/prod
- Monitor usage for anomalies
- Revoke compromised keys immediately
- Use project-specific keys
- Implement key rotation strategy

❌ DON'T:
- Hardcode keys in source code
- Commit keys to version control
- Share keys via email/chat
- Use the same key across environments
- Log full API keys
- Store keys in client-side code
- Share keys with unauthorized users
"""

print(security_checklist)
```

---

## 2. Rate Limiting

### 2.1 Understanding Rate Limits

```python
"""
03_rate_limiting.py - Handle rate limiting properly
"""

import os
import time
from dotenv import load_dotenv
from openai import OpenAI, RateLimitError

load_dotenv()
client = OpenAI()


def get_rate_limit_info(response):
    """Extract rate limit information from response headers"""
    # Note: In actual implementation, you'd need to access response headers
    # This is a simplified example
    return {
        "requests_limit": "10,000/min",
        "tokens_limit": "2,000,000/min",
        "requests_remaining": "9,998",
        "tokens_remaining": "1,999,500"
    }


def make_request_with_retry(prompt, max_retries=5):
    """Make request with exponential backoff retry logic"""
    base_delay = 1  # seconds

    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content

        except RateLimitError as e:
            if attempt < max_retries - 1:
                # Exponential backoff: 1s, 2s, 4s, 8s, 16s
                wait_time = base_delay * (2 ** attempt)
                print(f"Rate limit hit. Retrying in {wait_time}s... (Attempt {attempt + 1}/{max_retries})")
                time.sleep(wait_time)
            else:
                print(f"Max retries reached. Error: {e}")
                raise


class RateLimitManager:
    """Manage rate limits with token bucket algorithm"""

    def __init__(self, requests_per_minute=60, tokens_per_minute=90000):
        self.requests_per_minute = requests_per_minute
        self.tokens_per_minute = tokens_per_minute

        self.request_tokens = requests_per_minute
        self.token_tokens = tokens_per_minute

        self.last_update = time.time()

    def _refill_buckets(self):
        """Refill token buckets based on elapsed time"""
        now = time.time()
        elapsed = now - self.last_update

        # Refill based on time passed
        refill_rate_requests = self.requests_per_minute / 60  # per second
        refill_rate_tokens = self.tokens_per_minute / 60      # per second

        self.request_tokens = min(
            self.requests_per_minute,
            self.request_tokens + (refill_rate_requests * elapsed)
        )

        self.token_tokens = min(
            self.tokens_per_minute,
            self.token_tokens + (refill_rate_tokens * elapsed)
        )

        self.last_update = now

    def can_make_request(self, estimated_tokens=1000):
        """Check if request can be made"""
        self._refill_buckets()

        if self.request_tokens < 1:
            return False, "Request limit reached"

        if self.token_tokens < estimated_tokens:
            return False, "Token limit reached"

        return True, "OK"

    def consume(self, tokens_used):
        """Consume tokens after successful request"""
        self.request_tokens -= 1
        self.token_tokens -= tokens_used


# Rate Limiting Best Practices
rate_limit_guide = """
RATE LIMITING BEST PRACTICES:

1. Implement Exponential Backoff:
   - Wait 1s, then 2s, then 4s, etc.
   - Add jitter to avoid thundering herd

2. Monitor Rate Limit Headers:
   - x-ratelimit-limit-requests
   - x-ratelimit-remaining-requests
   - x-ratelimit-reset-requests

3. Batch Requests When Possible:
   - Group similar requests
   - Use batch API endpoints

4. Implement Request Queuing:
   - Queue requests locally
   - Process at controlled rate

5. Use Different Keys for Different Services:
   - Separate limits per service
   - Better isolation

Rate Limits by Tier:
- Free: 3 RPM (requests per minute)
- Tier 1: 500 RPM
- Tier 2: 5,000 RPM
- Tier 3: 10,000 RPM
- Tier 4+: Higher limits

TPM (Tokens Per Minute) limits vary by model.
"""

print(rate_limit_guide)
```

---

## 3. Request Debugging

### 3.1 Debugging Tools and Techniques

```python
"""
04_request_debugging.py - Debug API requests effectively
"""

import os
import json
import time
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()


def make_request_with_debugging(prompt):
    """Make request with detailed debugging information"""
    print("\n" + "="*60)
    print("REQUEST DEBUGGING")
    print("="*60)

    # Track request timing
    start_time = time.time()

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            # Add custom headers for tracking
            extra_headers={
                "X-Client-Request-Id": f"req_{int(time.time())}"
            }
        )

        end_time = time.time()
        duration = end_time - start_time

        # Print debugging information
        print(f"\n✅ Request Successful")
        print(f"Duration: {duration:.2f}s")
        print(f"Request ID: {response.id}")
        print(f"Model: {response.model}")
        print(f"Tokens Used: {response.usage.total_tokens}")
        print(f"  - Prompt: {response.usage.prompt_tokens}")
        print(f"  - Completion: {response.usage.completion_tokens}")

        return response

    except Exception as e:
        end_time = time.time()
        duration = end_time - start_time

        print(f"\n❌ Request Failed")
        print(f"Duration: {duration:.2f}s")
        print(f"Error Type: {type(e).__name__}")
        print(f"Error Message: {str(e)}")

        raise


class RequestLogger:
    """Log all API requests for debugging"""

    def __init__(self, log_file="api_requests.log"):
        self.log_file = log_file

    def log_request(self, prompt, response=None, error=None):
        """Log request details"""
        log_entry = {
            "timestamp": time.time(),
            "prompt": prompt[:100] + "..." if len(prompt) > 100 else prompt,
            "status": "success" if response else "error"
        }

        if response:
            log_entry.update({
                "request_id": response.id,
                "model": response.model,
                "tokens": response.usage.total_tokens
            })

        if error:
            log_entry.update({
                "error_type": type(error).__name__,
                "error_message": str(error)
            })

        # Append to log file
        with open(self.log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")

    def get_recent_logs(self, n=10):
        """Get recent log entries"""
        try:
            with open(self.log_file, "r") as f:
                lines = f.readlines()
                recent = lines[-n:] if len(lines) >= n else lines
                return [json.loads(line) for line in recent]
        except FileNotFoundError:
            return []


# Debugging Tips
debugging_tips = """
DEBUGGING TIPS:

1. Use Custom Request IDs:
   extra_headers={"X-Client-Request-Id": "your-id"}

2. Log All Requests:
   - Timestamp
   - Request parameters
   - Response details
   - Errors

3. Monitor Performance:
   - Track request duration
   - Token usage per request
   - Success/failure rates

4. Check Response Headers:
   - Request ID for support
   - Rate limit info
   - Processing time

5. Common Issues:
   - Invalid API key → Check env variables
   - Rate limiting → Implement backoff
   - Timeout → Increase timeout setting
   - Invalid model → Check model name

6. Use Verbose Logging During Development:
   - Print full requests/responses
   - Save to log files
   - Use structured logging

7. Test in Isolation:
   - Test API calls separately
   - Use curl to verify
   - Check API status page
"""

print(debugging_tips)
```

---

## 4. Multi-Organization Access

### 4.1 Managing Multiple Organizations

```python
"""
05_multi_org_access.py - Handle multiple organizations and projects
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class MultiOrgManager:
    """Manage API access across multiple organizations"""

    def __init__(self):
        self.organizations = {
            "personal": {
                "api_key": os.getenv("OPENAI_API_KEY_PERSONAL"),
                "org_id": os.getenv("OPENAI_ORG_ID_PERSONAL")
            },
            "work": {
                "api_key": os.getenv("OPENAI_API_KEY_WORK"),
                "org_id": os.getenv("OPENAI_ORG_ID_WORK")
            }
        }

    def get_client(self, org_name):
        """Get client for specific organization"""
        org_config = self.organizations.get(org_name)

        if not org_config:
            raise ValueError(f"Unknown organization: {org_name}")

        return OpenAI(
            api_key=org_config["api_key"],
            organization=org_config.get("org_id")
        )

    def make_request(self, org_name, prompt):
        """Make request using specific organization"""
        client = self.get_client(org_name)

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content


# Project-specific access
class ProjectManager:
    """Manage API access at project level"""

    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.projects = {
            "chatbot": os.getenv("OPENAI_PROJECT_CHATBOT"),
            "analytics": os.getenv("OPENAI_PROJECT_ANALYTICS"),
            "research": os.getenv("OPENAI_PROJECT_RESEARCH")
        }

    def get_client(self, project_name):
        """Get client for specific project"""
        project_id = self.projects.get(project_name)

        if not project_id:
            raise ValueError(f"Unknown project: {project_name}")

        return OpenAI(
            api_key=self.api_key,
            project=project_id
        )


# Usage example
multi_org_guide = """
MULTI-ORGANIZATION ACCESS:

Setup:
1. Create separate API keys for each org
2. Store in separate environment variables
3. Use organization-specific clients

Environment Variables:
OPENAI_API_KEY_PERSONAL=sk-proj-...
OPENAI_ORG_ID_PERSONAL=org-...
OPENAI_API_KEY_WORK=sk-proj-...
OPENAI_ORG_ID_WORK=org-...

Project-Level Access:
OPENAI_API_KEY=sk-proj-...
OPENAI_PROJECT_CHATBOT=proj-...
OPENAI_PROJECT_ANALYTICS=proj-...

Benefits:
- Separate billing
- Different rate limits
- Access control
- Usage tracking per org/project

Best Practices:
- Use project keys when possible
- Implement least privilege
- Monitor usage per org/project
- Rotate keys regularly
"""

print(multi_org_guide)
```

---

## 5. API Versioning

### 5.1 Backward Compatibility

```python
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
```

---

## 6. Best Practices

### 6.1 Production-Ready API Integration

```python
"""
07_best_practices.py - Production best practices
"""

import os
import time
import hashlib
from functools import wraps
from dotenv import load_dotenv
from openai import OpenAI, APIError

load_dotenv()
client = OpenAI()


def with_retry(max_retries=3, base_delay=1):
    """Decorator for automatic retry with exponential backoff"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except APIError as e:
                    if attempt < max_retries - 1:
                        wait_time = base_delay * (2 ** attempt)
                        print(f"Retry {attempt + 1}/{max_retries} in {wait_time}s")
                        time.sleep(wait_time)
                    else:
                        raise
            return None
        return wrapper
    return decorator


def with_caching(cache_duration=3600):
    """Decorator for caching responses"""
    cache = {}

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key
            cache_key = hashlib.md5(
                f"{func.__name__}:{args}:{kwargs}".encode()
            ).hexdigest()

            # Check cache
            if cache_key in cache:
                cached_value, cached_time = cache[cache_key]
                if time.time() - cached_time < cache_duration:
                    print("✅ Returning cached result")
                    return cached_value

            # Call function
            result = func(*args, **kwargs)

            # Cache result
            cache[cache_key] = (result, time.time())

            return result
        return wrapper
    return decorator


class ProductionAPIClient:
    """Production-ready API client with best practices"""

    def __init__(self):
        self.client = OpenAI()
        self.request_log = []

    @with_retry(max_retries=3)
    @with_caching(cache_duration=3600)
    def make_request(self, prompt, **kwargs):
        """Make API request with retry and caching"""
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            **kwargs
        )

        # Log request
        self.request_log.append({
            "timestamp": time.time(),
            "tokens": response.usage.total_tokens,
            "model": response.model
        })

        return response.choices[0].message.content

    def get_usage_stats(self):
        """Get usage statistics"""
        if not self.request_log:
            return {"total_requests": 0, "total_tokens": 0}

        return {
            "total_requests": len(self.request_log),
            "total_tokens": sum(log["tokens"] for log in self.request_log),
            "avg_tokens": sum(log["tokens"] for log in self.request_log) / len(self.request_log)
        }


best_practices_summary = """
PRODUCTION BEST PRACTICES SUMMARY:

1. ERROR HANDLING:
   ✅ Implement retry logic with exponential backoff
   ✅ Handle specific exception types
   ✅ Log errors with context
   ✅ Provide fallback responses

2. PERFORMANCE:
   ✅ Cache common responses
   ✅ Use appropriate models (don't over-provision)
   ✅ Set reasonable timeouts
   ✅ Implement request batching

3. MONITORING:
   ✅ Track token usage
   ✅ Monitor error rates
   ✅ Log request/response times
   ✅ Set up alerting

4. SECURITY:
   ✅ Never expose API keys
   ✅ Use environment variables
   ✅ Rotate keys regularly
   ✅ Implement rate limiting client-side

5. RELIABILITY:
   ✅ Implement circuit breakers
   ✅ Use health checks
   ✅ Plan for API downtime
   ✅ Have fallback strategies

6. COST OPTIMIZATION:
   ✅ Cache responses when possible
   ✅ Use appropriate model tiers
   ✅ Set max_tokens limits
   ✅ Monitor and set budgets

7. TESTING:
   ✅ Write unit tests
   ✅ Mock API calls in tests
   ✅ Test error scenarios
   ✅ Load test before production

8. DOCUMENTATION:
   ✅ Document API usage
   ✅ Version your integrations
   ✅ Keep API key docs secure
   ✅ Maintain changelog
"""

print(best_practices_summary)
```

---

## Summary

✅ **Key Learnings**:
- Multiple authentication methods and security
- Rate limiting strategies and handling
- Effective debugging techniques
- Multi-organization and project management
- API versioning and compatibility
- Production best practices

✅ **Skills Acquired**:
- Secure API key management
- Rate limit handling with exponential backoff
- Request debugging and logging
- Multi-org access patterns
- Version management

---

[⬅️ Previous: Module 3](../module-03-core-concepts/README.md) | [Home](../README.md) | [Next: Module 5 ➡️](../module-05-platform-apis/README.md)
