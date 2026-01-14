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
"""

print(best_practices_summary)
