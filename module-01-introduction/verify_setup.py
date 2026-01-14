"""
verify_setup.py - Verify your OpenAI setup is working correctly

This script checks that your development environment is properly configured
for working with the OpenAI API.
"""

import os
import sys
from dotenv import load_dotenv


def verify_python_version():
    """Check Python version is 3.8+"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"❌ Python version: {version.major}.{version.minor}.{version.micro} (requires 3.8+)")
        return False


def verify_openai_package():
    """Check OpenAI package is installed"""
    try:
        import openai
        print(f"✅ OpenAI package installed: v{openai.__version__}")
        return True
    except ImportError:
        print("❌ OpenAI package not installed")
        print("   Run: pip install openai")
        return False


def verify_dotenv_package():
    """Check python-dotenv package is installed"""
    try:
        import dotenv
        print(f"✅ python-dotenv package installed")
        return True
    except ImportError:
        print("❌ python-dotenv package not installed")
        print("   Run: pip install python-dotenv")
        return False


def verify_api_key():
    """Check API key is configured"""
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    if api_key:
        # Don't print the full key for security
        if len(api_key) > 12:
            masked_key = f"{api_key[:8]}...{api_key[-4:]}"
        else:
            masked_key = "***"
        print(f"✅ API key found: {masked_key}")

        # Validate key format
        if api_key.startswith("sk-"):
            print(f"   Key format appears valid")
            return True
        else:
            print(f"   ⚠️  Warning: Key doesn't start with 'sk-', may be invalid")
            return False
    else:
        print("❌ API key not found")
        print("   Set OPENAI_API_KEY environment variable or create .env file")
        return False


def test_api_connection():
    """Test actual API connection"""
    try:
        from openai import OpenAI

        load_dotenv()
        client = OpenAI()

        # Simple API call to test connection
        print("\n🔄 Testing API connection...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Say 'Hello!' if you can hear me."}],
            max_tokens=10
        )

        print(f"✅ API connection successful!")
        print(f"   Model used: {response.model}")
        print(f"   Response: {response.choices[0].message.content}")
        return True

    except Exception as e:
        print(f"❌ API connection failed: {str(e)}")
        return False


def main():
    """Run all verification checks"""
    print("=" * 60)
    print("OpenAI Setup Verification")
    print("=" * 60 + "\n")

    checks = [
        ("Python Version", verify_python_version),
        ("OpenAI Package", verify_openai_package),
        ("Python-dotenv Package", verify_dotenv_package),
        ("API Key Configuration", verify_api_key),
    ]

    results = []
    for name, check_func in checks:
        result = check_func()
        results.append(result)
        print()

    # Only test API connection if basic checks pass
    if all(results):
        api_result = test_api_connection()
        results.append(api_result)
        print()

    print("=" * 60)
    if all(results):
        print("🎉 All checks passed! You're ready to start building with OpenAI!")
    else:
        print("⚠️  Some checks failed. Please fix the issues above.")
        print("\nTroubleshooting Tips:")
        print("1. Ensure Python 3.8+ is installed")
        print("2. Install required packages: pip install openai python-dotenv")
        print("3. Create a .env file with: OPENAI_API_KEY=your-key-here")
        print("4. Get your API key from: https://platform.openai.com/api-keys")
    print("=" * 60)


if __name__ == "__main__":
    main()
