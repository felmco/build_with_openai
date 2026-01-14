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
