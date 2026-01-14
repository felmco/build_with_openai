# Module 1: Introduction and Setup

## 📋 Module Overview

**Duration**: 30 minutes
**Level**: Beginner
**Prerequisites**: None

Welcome to Module 1! In this module, you'll learn about OpenAI, understand the platform architecture, and set up your development environment. By the end of this module, you'll be ready to make your first API call.

---

## 🎯 Learning Objectives

By the end of this module, you will be able to:
- ✅ Explain what OpenAI is and its key capabilities
- ✅ Understand the OpenAI platform architecture
- ✅ Set up a Python development environment
- ✅ Create and secure API keys
- ✅ Install and configure the OpenAI Python SDK
- ✅ Verify your setup is working correctly

---

## 📖 Table of Contents

1. [What is OpenAI?](#what-is-openai)
2. [Understanding the OpenAI Platform](#understanding-the-openai-platform)
3. [Setting Up Your Development Environment](#setting-up-your-development-environment)
4. [API Key Management](#api-key-management)
5. [Installing the OpenAI Python SDK](#installing-the-openai-python-sdk)
6. [Verifying Your Setup](#verifying-your-setup)
7. [Exercises](#exercises)
8. [Summary](#summary)

---

## What is OpenAI?

### Overview

**OpenAI** is an artificial intelligence research laboratory and technology company that develops cutting-edge AI models and provides them through accessible APIs. Founded with the mission to ensure artificial general intelligence (AGI) benefits all of humanity, OpenAI creates powerful AI tools that developers can integrate into their applications.

### Key Capabilities

OpenAI's platform provides several core capabilities:

#### 1. **Text Generation**
Generate human-like text for various purposes:
- Content creation (articles, stories, emails)
- Question answering
- Summarization
- Translation
- Conversation and chatbots

#### 2. **Code Generation**
AI-powered coding assistance:
- Write code from natural language descriptions
- Debug and fix code issues
- Explain code functionality
- Refactor and optimize code

#### 3. **Vision & Image Analysis**
Analyze and generate visual content:
- Image understanding and description
- Object detection
- Visual question answering
- Image generation from text descriptions (DALL-E)

#### 4. **Audio Processing**
Work with audio and speech:
- Speech-to-text transcription (Whisper)
- Text-to-speech generation
- Audio analysis

#### 5. **Embeddings**
Create semantic representations:
- Text similarity comparison
- Semantic search
- Clustering and classification
- Recommendation systems

### Why Use OpenAI?

#### For Developers:
- **Easy Integration**: RESTful APIs with SDKs in multiple languages
- **Powerful Models**: Access to state-of-the-art AI models
- **Scalable**: From prototype to production with the same API
- **Well-Documented**: Comprehensive documentation and examples

#### For Businesses:
- **Time-to-Market**: Build AI features without training models from scratch
- **Cost-Effective**: Pay-per-use pricing model
- **Reliable**: Enterprise-grade infrastructure
- **Flexible**: Customize models with fine-tuning

#### For Innovation:
- **Rapid Prototyping**: Test AI ideas quickly
- **Versatile**: One platform for multiple AI capabilities
- **Community**: Large developer community and resources

---

## Understanding the OpenAI Platform

### Platform Architecture

The OpenAI platform consists of several layers:

```
┌─────────────────────────────────────────┐
│        Your Application                 │
│  (Web App, Mobile App, Service, etc.)  │
└─────────────────────────────────────────┘
                 ↓ ↑
┌─────────────────────────────────────────┐
│         OpenAI SDKs/Libraries          │
│    (Python, JavaScript, C#, etc.)      │
└─────────────────────────────────────────┘
                 ↓ ↑
┌─────────────────────────────────────────┐
│           OpenAI REST API              │
│  (HTTP/HTTPS Requests & Responses)     │
└─────────────────────────────────────────┘
                 ↓ ↑
┌─────────────────────────────────────────┐
│          OpenAI Platform               │
│  - Model Inference                     │
│  - Rate Limiting                       │
│  - Authentication                      │
│  - Usage Tracking                      │
└─────────────────────────────────────────┘
                 ↓ ↑
┌─────────────────────────────────────────┐
│          AI Models                     │
│  GPT-5.2, GPT-5 mini, GPT-5 nano, etc. │
└─────────────────────────────────────────┘
```

### Key Components

#### 1. **API Endpoints**
The platform provides RESTful HTTP endpoints:
- `https://api.openai.com/v1/` - Base URL for all API calls
- Different endpoints for different capabilities (chat, images, audio, etc.)

#### 2. **Authentication**
Secure access via API keys:
- Organization-level keys
- Project-specific keys
- Service account keys

#### 3. **Models**
Multiple AI models with different capabilities:
- **GPT-5.2**: Latest and most capable model
- **GPT-5 mini**: Fast and cost-efficient
- **GPT-5 nano**: Fastest and most economical
- **Specialized models**: For images, audio, embeddings

#### 4. **Rate Limits**
Controlled access to ensure fair usage:
- Requests per minute (RPM)
- Tokens per minute (TPM)
- Tier-based limits based on usage history

#### 5. **Usage Tracking**
Monitor and manage your API usage:
- Token consumption
- Cost tracking
- Request logging

---

## Setting Up Your Development Environment

### System Requirements

Before you begin, ensure you have:
- **Operating System**: Windows, macOS, or Linux
- **Python**: Version 3.8 or higher
- **Internet Connection**: For API calls
- **Text Editor/IDE**: VS Code, PyCharm, or any editor of your choice

### Step 1: Check Python Installation

Open your terminal or command prompt and verify Python is installed:

```bash
python --version
# or
python3 --version
```

You should see output like: `Python 3.8.x` or higher.

**If Python is not installed**:
- **Windows**: Download from [python.org](https://www.python.org/downloads/)
- **macOS**: Use Homebrew: `brew install python3`
- **Linux**: Use your package manager: `sudo apt install python3 python3-pip`

### Step 2: Verify pip Installation

pip is Python's package installer. Verify it's installed:

```bash
pip --version
# or
pip3 --version
```

### Step 3: Create a Project Directory

Create a dedicated directory for your OpenAI projects:

```bash
# Create directory
mkdir openai-course
cd openai-course

# Create a subdirectory for module 1
mkdir module-01
cd module-01
```

### Step 4: Set Up a Virtual Environment (Recommended)

Virtual environments help manage dependencies and avoid conflicts:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

When activated, you'll see `(venv)` in your terminal prompt.

### Step 5: Install Essential Packages

```bash
# Upgrade pip
pip install --upgrade pip

# Install essential packages
pip install openai python-dotenv requests
```

**Packages installed**:
- `openai`: Official OpenAI Python SDK
- `python-dotenv`: Load environment variables from .env files
- `requests`: HTTP library (useful for API exploration)

---

## API Key Management

### Creating Your OpenAI Account

1. Visit [https://platform.openai.com/signup](https://platform.openai.com/signup)
2. Sign up with your email or continue with Google/Microsoft
3. Verify your email address
4. Complete the onboarding process

### Generating an API Key

1. Log in to your OpenAI account
2. Navigate to [API Keys](https://platform.openai.com/api-keys)
3. Click "Create new secret key"
4. Give your key a descriptive name (e.g., "development-key")
5. **IMPORTANT**: Copy the key immediately - you won't be able to see it again!
6. Store the key securely

### API Key Security Best Practices

#### ⚠️ CRITICAL SECURITY RULES

1. **Never hardcode API keys in your code**
   ```python
   # ❌ NEVER DO THIS
   api_key = "sk-proj-abc123..."
   ```

2. **Never commit API keys to version control**
   ```bash
   # Always add .env to .gitignore
   echo ".env" >> .gitignore
   ```

3. **Use environment variables**
   ```python
   # ✅ CORRECT WAY
   import os
   api_key = os.getenv("OPENAI_API_KEY")
   ```

4. **Rotate keys regularly** - Generate new keys periodically

5. **Use project-specific keys** - Different keys for dev, staging, production

6. **Monitor usage** - Watch for unexpected usage patterns

### Setting Up Environment Variables

#### Method 1: Using .env File (Recommended for Development)

1. Create a `.env` file in your project root:
   ```bash
   touch .env
   ```

2. Add your API key to `.env`:
   ```
   OPENAI_API_KEY=sk-proj-your-actual-key-here
   ```

3. Add `.env` to `.gitignore`:
   ```bash
   echo ".env" >> .gitignore
   ```

4. Load in your Python code:
   ```python
   from dotenv import load_dotenv
   import os

   load_dotenv()
   api_key = os.getenv("OPENAI_API_KEY")
   ```

#### Method 2: System Environment Variables

**On macOS/Linux**:
```bash
# Add to ~/.bashrc or ~/.zshrc
export OPENAI_API_KEY="sk-proj-your-actual-key-here"

# Reload shell configuration
source ~/.bashrc  # or source ~/.zshrc
```

**On Windows**:
```cmd
# Command Prompt
setx OPENAI_API_KEY "sk-proj-your-actual-key-here"

# PowerShell
[System.Environment]::SetEnvironmentVariable('OPENAI_API_KEY', 'sk-proj-your-actual-key-here', 'User')
```

---

## Installing the OpenAI Python SDK

### Installation

The OpenAI Python SDK provides a convenient way to interact with the OpenAI API:

```bash
pip install openai
```

### Verifying Installation

```bash
pip show openai
```

You should see package information including version number (should be 1.0.0 or higher).

### SDK Features

The Python SDK provides:
- **Type hints**: Better IDE support and fewer errors
- **Async support**: For concurrent requests
- **Automatic retries**: Handle transient failures
- **Error handling**: Clear exception classes
- **Streaming support**: Real-time response streaming

---

## Verifying Your Setup

### Quick Verification Script

Create a file called `verify_setup.py`:

```python
"""
verify_setup.py - Verify your OpenAI setup is working correctly
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

def verify_api_key():
    """Check API key is configured"""
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    if api_key:
        # Don't print the full key for security
        masked_key = f"{api_key[:8]}...{api_key[-4:]}"
        print(f"✅ API key found: {masked_key}")
        return True
    else:
        print("❌ API key not found")
        print("   Set OPENAI_API_KEY environment variable")
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
        ("API Key", verify_api_key),
        ("API Connection", test_api_connection),
    ]

    results = []
    for name, check_func in checks:
        result = check_func()
        results.append(result)
        print()

    print("=" * 60)
    if all(results):
        print("🎉 All checks passed! You're ready to start building with OpenAI!")
    else:
        print("⚠️  Some checks failed. Please fix the issues above.")
    print("=" * 60)

if __name__ == "__main__":
    main()
```

### Running the Verification Script

```bash
python verify_setup.py
```

**Expected Output** (if everything is set up correctly):
```
============================================================
OpenAI Setup Verification
============================================================

✅ Python version: 3.11.5
✅ OpenAI package installed: v1.12.0
✅ API key found: sk-proj-...ab12

🔄 Testing API connection...
✅ API connection successful!
   Response: Hello!

============================================================
🎉 All checks passed! You're ready to start building with OpenAI!
============================================================
```

---

## Exercises

### Exercise 1: Environment Setup
1. Create a new directory for OpenAI projects
2. Set up a virtual environment
3. Install the OpenAI SDK
4. Create a `.env` file with your API key
5. Run the verification script

### Exercise 2: Security Audit
Review the following code and identify security issues:

```python
# example.py
import openai

openai.api_key = "sk-proj-abc123xyz"

def generate_text(prompt):
    response = openai.Completion.create(
        model="gpt-3.5-turbo",
        prompt=prompt
    )
    return response
```

**Questions**:
1. What security issues do you see?
2. How would you fix them?
3. What other best practices should be applied?

### Exercise 3: Documentation Exploration
Visit the [OpenAI Documentation](https://platform.openai.com/docs) and answer:
1. What are the current GPT model versions available?
2. What is the difference between GPT-5.2 and GPT-5 mini?
3. What are the main API endpoints available?

---

## Summary

### Key Takeaways

✅ **What We Learned**:
- OpenAI provides powerful AI capabilities through easy-to-use APIs
- The platform supports text, code, images, audio, and embeddings
- Proper setup includes Python, SDK installation, and API key configuration
- Security is critical - never expose API keys in code or version control
- The Python SDK provides a convenient interface to the OpenAI API

✅ **Skills Acquired**:
- Set up Python development environment
- Install and configure OpenAI SDK
- Manage API keys securely
- Verify setup is working correctly

### Next Steps

You're now ready to make your first API calls! In **Module 2: Getting Started with OpenAI API**, you'll:
- Make your first API request
- Understand model selection
- Learn about request parameters
- Build a simple chatbot

---

## Additional Resources

- 📚 [Official OpenAI Documentation](https://platform.openai.com/docs)
- 🔑 [API Keys Management](https://platform.openai.com/api-keys)
- 💬 [OpenAI Community Forum](https://community.openai.com/)
- 📖 [OpenAI Cookbook](https://github.com/openai/openai-cookbook)
- 🐍 [Python SDK GitHub](https://github.com/openai/openai-python)

---

## Knowledge Check

Test your understanding:

1. What are the three main ways to use OpenAI's capabilities?
2. Why should you never hardcode API keys in your source code?
3. What is the purpose of a virtual environment?
4. Name three core capabilities of the OpenAI platform.
5. What command verifies your Python installation?

**Answers are at the bottom of this file**

---

[⬅️ Back to Course Home](../README.md) | [Next: Module 2 - Getting Started ➡️](../module-02-getting-started/README.md)

---

### Knowledge Check Answers

1. Text generation, code generation, and image/vision processing (also audio and embeddings)
2. To prevent unauthorized access if code is shared or committed to version control
3. To isolate project dependencies and avoid conflicts between projects
4. Any three of: Text Generation, Code Generation, Vision & Images, Audio & Speech, Embeddings
5. `python --version` or `python3 --version`
