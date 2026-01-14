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
# client_explicit = OpenAI(api_key="sk-proj-your-key-here")


# Method 3: Organization and Project specific
# client_org = OpenAI(
#     api_key=os.getenv("OPENAI_API_KEY"),
#     organization=os.getenv("OPENAI_ORG_ID"),  # Optional
#     project=os.getenv("OPENAI_PROJECT_ID")     # Optional
# )


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
