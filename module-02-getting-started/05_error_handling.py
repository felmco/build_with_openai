"""
05_error_handling.py - Handle API errors gracefully
"""

import os
from dotenv import load_dotenv
from openai import OpenAI, APIError, RateLimitError, APIConnectionError

load_dotenv()
# Intentionally using a bad key to trigger authentication error for demonstration
# client = OpenAI(api_key="invalid-key") 
client = OpenAI()

def make_safe_request():
    try:
        response = client.chat.completions.create(
            model="gpt-5-mini",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=50
        )
        print("Success:", response.choices[0].message.content)
        
    except RateLimitError as e:
        print("Error: Rate limit exceeded.")
        print(f"Details: {e}")
        # Implement backoff logic here
        
    except APIConnectionError as e:
        print("Error: Could not connect to OpenAI API.")
        print(f"Check your internet connection.")
        
    except APIError as e:
        print(f"Error: OpenAI API returned an API Error: {e}")
        
    except Exception as e:
        print(f"Unexpected error: {e}")


def main():
    print("Demonstrating error handling...")
    make_safe_request()


if __name__ == "__main__":
    main()
