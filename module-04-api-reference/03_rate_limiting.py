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
