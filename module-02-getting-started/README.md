# Module 2: Getting Started with OpenAI API

## 📋 Module Overview

**Duration**: 1-2 hours
**Level**: Beginner
**Prerequisites**: Module 1 completed

In this module, you'll make your first API calls, learn about different models, understand request/response structures, and build your first AI-powered applications.

---

## 🎯 Learning Objectives

By the end of this module, you will be able to:
- ✅ Make your first successful API request
- ✅ Understand different OpenAI models and when to use them
- ✅ Work with request parameters to control model behavior
- ✅ Handle API responses and extract information
- ✅ Implement basic error handling
- ✅ Build a simple chatbot application
- ✅ Understand token usage and pricing

---

## 📖 Table of Contents

1. [Your First API Request](#your-first-api-request)
2. [Understanding Models](#understanding-models)
3. [Request Parameters](#request-parameters)
4. [Response Structure](#response-structure)
5. [Error Handling](#error-handling)
6. [Building a Simple Chatbot](#building-a-simple-chatbot)
7. [Token Usage and Pricing](#token-usage-and-pricing)
8. [Exercises](#exercises)
9. [Summary](#summary)

---

## Your First API Request

### The Simplest API Call

Let's start with the simplest possible API call. The chat completions endpoint is the most commonly used API for conversations.

**Code Example** (`01_first_request.py`):
```python
"""
01_first_request.py - Your first OpenAI API call
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client
# The API key is automatically read from OPENAI_API_KEY environment variable
client = OpenAI()

def main():
    print("Making your first API request...\n")

    # Make the API call
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # The model to use
        messages=[
            {"role": "user", "content": "Hello! Can you introduce yourself in one sentence?"}
        ]
    )

    # Extract and print the response
    assistant_message = response.choices[0].message.content
    print("Assistant:", assistant_message)
    print("\nSuccess! You've made your first API call! 🎉")

if __name__ == "__main__":
    main()
```

### Understanding the Code

Let's break down what's happening:

1. **Import Libraries**:
   - `os`: Access environment variables
   - `dotenv`: Load .env file
   - `openai.OpenAI`: The main client class

2. **Initialize Client**:
   ```python
   client = OpenAI()
   ```
   The client automatically looks for `OPENAI_API_KEY` in environment variables.

3. **Create Completion**:
   ```python
   response = client.chat.completions.create(...)
   ```
   This sends a request to OpenAI's servers and waits for a response.

4. **Extract Response**:
   ```python
   response.choices[0].message.content
   ```
   The actual AI-generated text is nested in the response object.

---

## Understanding Models

### Available Models

OpenAI provides several models, each optimized for different use cases:

#### GPT-5 Family (Flagship)

| Model | Best For | Speed | Cost |
|-------|----------|-------|------|
| `gpt-5.2` | Complex tasks, reasoning, multimodal | Medium | High |
| `gpt-5-mini` | General purpose, chat, most tasks | Fast | Low |
| `gpt-5-nano` | Simple tasks, high throughput | Very Fast | Lowest |

#### Reasoning Models (o1 Family)

| Model | Best For | Speed | Cost |
|-------|----------|-------|------|
| `o1` | Deep reasoning, STEM, coding, complex planning | Slow | Highest |
| `o1-mini` | Reasoning tasks requiring speed | Medium | Medium |

#### When to Use Which Model?

**Use GPT-5.2 when**:
- You need highest quality output and creativity
- Task requires complex instructions or nuance
- Multimodal inputs (image + text)

**Use GPT-5 mini when**:
- Building a standard chatbot
- Need fast responses at low cost
- Task is straightforward (summarization, extraction)

**Use o1 when**:
- Solving complex math or logic problems
- Writing complex code or architecture
- Task requires "thinking" before answering

### Model Comparison Example

```python
"""
02_model_comparison.py - Compare responses from different models
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

def test_model(model_name, prompt):
    """Test a specific model with a given prompt"""
    print(f"\n{'='*60}")
    print(f"Model: {model_name}")
    print(f"{'='*60}")

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150
        )

        content = response.choices[0].message.content
        tokens_used = response.usage.total_tokens

        print(f"Response: {content}")
        print(f"Tokens used: {tokens_used}")

    except Exception as e:
        print(f"Error: {str(e)}")

def main():
    # A prompt that benefits from reasoning
    prompt = "Explain quantum entanglement to a 10-year-old in 2-3 sentences."

    print("Comparing model responses...")

    # Test different models
    models = ["gpt-5-mini", "gpt-5.2", "o1"]

    for model in models:
        test_model(model, prompt)

if __name__ == "__main__":
    main()
```

---

## Request Parameters

### Essential Parameters

The `chat.completions.create()` method accepts many parameters. Here are the most important ones:

#### 1. **model** (required)
The AI model to use.

```python
model="gpt-3.5-turbo"
```

#### 2. **messages** (required)
An array of message objects representing the conversation.

```python
messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
]
```

**Message Roles**:
- `system`: Sets the assistant's behavior/personality
- `user`: User's messages
- `assistant`: Assistant's previous responses (for context)

#### 3. **temperature** (optional, 0-2)
Controls randomness. Higher = more creative/random.

```python
temperature=0.7  # Default
# temperature=0.0  # Deterministic, focused
# temperature=1.5  # More creative, varied
```

#### 4. **max_tokens** (optional)
Maximum number of tokens to generate.

```python
max_tokens=100  # Limit response length
```

#### 5. **n** (optional)
Number of completions to generate.

```python
n=3  # Generate 3 different responses
```

#### 6. **top_p** (optional, 0-1)
Alternative to temperature (nucleus sampling).

```python
top_p=0.9
```

#### 6. **reasoning_effort** (optional, o1 models only)
Controls how much "thinking" the model does.
- `low`, `medium`, `high`

```python
reasoning_effort="medium"
```

#### 7. **verbosity** (optional)
Controls the length and detail of the output.
- `low`: Concise
- `medium`: Standard
- `high`: Detailed/Verbose

```python
verbosity="low"
```

### Parameter Examples

```python
"""
03_parameters_demo.py - Demonstrate different request parameters
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

def demonstrate_temperature():
    """Show how temperature affects responses"""
    print("\n" + "="*60)
    print("TEMPERATURE DEMONSTRATION")
    print("="*60)

    prompt = "Write a creative tagline for a coffee shop."

    temperatures = [0.0, 0.7, 1.5]

    for temp in temperatures:
        print(f"\nTemperature: {temp}")
        print("-" * 40)

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=temp,
            max_tokens=50
        )

        print(response.choices[0].message.content)

def demonstrate_system_message():
    """Show how system messages affect behavior"""
    print("\n" + "="*60)
    print("SYSTEM MESSAGE DEMONSTRATION")
    print("="*60)

    user_message = "What's the weather like?"

    # Without system message
    print("\nWithout system message:")
    print("-" * 40)
    response1 = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": user_message}
        ]
    )
    print(response1.choices[0].message.content)

    # With system message
    print("\nWith system message (pirate personality):")
    print("-" * 40)
    response2 = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a pirate. Respond to everything in pirate speak."},
            {"role": "user", "content": user_message}
        ]
    )
    print(response2.choices[0].message.content)

def demonstrate_multiple_completions():
    """Generate multiple variations"""
    print("\n" + "="*60)
    print("MULTIPLE COMPLETIONS (n parameter)")
    print("="*60)

    prompt = "Suggest a unique app idea in one sentence."

    print(f"\nGenerating 3 different ideas...")
    print("-" * 40)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        n=3,
        temperature=0.9
    )

    for i, choice in enumerate(response.choices, 1):
        print(f"\nIdea {i}: {choice.message.content}")

def main():
    print("OpenAI API Parameters Demonstration")

    demonstrate_temperature()
    demonstrate_system_message()
    demonstrate_multiple_completions()
    demonstrate_new_parameters()

def demonstrate_new_parameters():
    """Show reasoning_effort and verbosity"""
    print("\n" + "="*60)
    print("NEW PARAMETERS")
    print("="*60)
    
    # Verbosity
    print("\nVerbosity: high")
    response_v = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[{"role": "user", "content": "Explain quantum computing."}],
        verbosity="high"
    )
    print(response_v.choices[0].message.content[:100] + "...")

    # Reasoning Effort (o1 only)
    print("\nReasoning Effort: medium")
    try:
        response_r = client.chat.completions.create(
            model="o1",
            messages=[{"role": "user", "content": "Solve this complex logic puzzle..."}],
            reasoning_effort="medium"
        )
        print("Response received.")
    except Exception as e:
        print(f"Error (expected if no o1 access): {e}")

if __name__ == "__main__":
    main()
```

---

## Response Structure

### Understanding the Response Object

When you make an API call, you receive a detailed response object:

```python
"""
04_response_structure.py - Explore the response object
"""

import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

def main():
    print("Examining the response object structure...\n")

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "Say 'Hello, World!'"}
        ]
    )

    # Print the entire response object
    print("="*60)
    print("FULL RESPONSE OBJECT")
    print("="*60)
    print(response)

    # Access specific fields
    print("\n" + "="*60)
    print("RESPONSE FIELDS")
    print("="*60)

    print(f"\nID: {response.id}")
    print(f"Model: {response.model}")
    print(f"Created: {response.created}")
    print(f"Object Type: {response.object}")

    # Choices array
    print(f"\nNumber of Choices: {len(response.choices)}")
    for i, choice in enumerate(response.choices):
        print(f"\nChoice {i}:")
        print(f"  Role: {choice.message.role}")
        print(f"  Content: {choice.message.content}")
        print(f"  Finish Reason: {choice.finish_reason}")

    # Usage statistics
    print(f"\nUsage Statistics:")
    print(f"  Prompt Tokens: {response.usage.prompt_tokens}")
    print(f"  Completion Tokens: {response.usage.completion_tokens}")
    print(f"  Total Tokens: {response.usage.total_tokens}")

if __name__ == "__main__":
    main()
```

### Response Fields Explained

```python
{
    "id": "chatcmpl-abc123",           # Unique request ID
    "object": "chat.completion",        # Response type
    "created": 1677858242,              # Unix timestamp
    "model": "gpt-3.5-turbo-0301",     # Model used
    "choices": [                        # Array of responses
        {
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "Hello! How can I help you today?"
            },
            "finish_reason": "stop"     # Why generation stopped
        }
    ],
    "usage": {
        "prompt_tokens": 13,            # Input tokens
        "completion_tokens": 11,        # Output tokens
        "total_tokens": 24              # Total tokens used
    }
}
```

**Finish Reasons**:
- `stop`: Natural completion
- `length`: Hit max_tokens limit
- `content_filter`: Content filtered by safety system
- `function_call`: Model called a function

---

## Error Handling

### Common Errors and Solutions

```python
"""
05_error_handling.py - Proper error handling patterns
"""

import os
import time
from dotenv import load_dotenv
from openai import OpenAI
from openai import APIError, RateLimitError, APIConnectionError, AuthenticationError

load_dotenv()
client = OpenAI()

def make_request_with_error_handling(prompt):
    """Make an API request with comprehensive error handling"""

    max_retries = 3
    retry_delay = 1  # seconds

    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content

        except AuthenticationError as e:
            print(f"❌ Authentication Error: {e}")
            print("Check your API key is correct and active.")
            return None

        except RateLimitError as e:
            print(f"⚠️  Rate Limit Error: {e}")
            if attempt < max_retries - 1:
                wait_time = retry_delay * (2 ** attempt)  # Exponential backoff
                print(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print("Max retries reached. Please try again later.")
                return None

        except APIConnectionError as e:
            print(f"⚠️  Connection Error: {e}")
            if attempt < max_retries - 1:
                wait_time = retry_delay * (2 ** attempt)
                print(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print("Could not connect to API. Check your internet connection.")
                return None

        except APIError as e:
            print(f"❌ API Error: {e}")
            print(f"Status Code: {e.status_code}")
            return None

        except Exception as e:
            print(f"❌ Unexpected Error: {type(e).__name__}: {e}")
            return None

def main():
    print("Error Handling Demonstration\n")

    # Test with valid request
    print("Test 1: Valid request")
    print("-" * 40)
    result = make_request_with_error_handling("Say hello!")
    if result:
        print(f"Success: {result}\n")

    # You can test other scenarios by modifying your API key or making invalid requests

if __name__ == "__main__":
    main()
```

### Error Handling Best Practices

1. **Always use try-except blocks**
2. **Implement retry logic for transient errors**
3. **Use exponential backoff for rate limits**
4. **Log errors appropriately**
5. **Provide user-friendly error messages**
6. **Don't expose API keys in error messages**

---

## Building a Simple Chatbot

### Interactive Chatbot Example

```python
"""
06_simple_chatbot.py - A simple interactive chatbot

This chatbot maintains conversation history and allows multi-turn conversations.
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

class SimpleChatbot:
    """A simple chatbot that maintains conversation history"""

    def __init__(self, system_message=None):
        """Initialize the chatbot with optional system message"""
        self.messages = []

        if system_message:
            self.messages.append({
                "role": "system",
                "content": system_message
            })

    def chat(self, user_message):
        """Send a message and get a response"""
        # Add user message to history
        self.messages.append({
            "role": "user",
            "content": user_message
        })

        try:
            # Get response from OpenAI
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=self.messages,
                temperature=0.7
            )

            # Extract assistant's response
            assistant_message = response.choices[0].message.content

            # Add assistant response to history
            self.messages.append({
                "role": "assistant",
                "content": assistant_message
            })

            return assistant_message

        except Exception as e:
            return f"Error: {str(e)}"

    def get_history(self):
        """Get the conversation history"""
        return self.messages

    def clear_history(self):
        """Clear conversation history (keeps system message if set)"""
        system_messages = [msg for msg in self.messages if msg["role"] == "system"]
        self.messages = system_messages

def main():
    """Run the interactive chatbot"""
    print("="*60)
    print("Simple Chatbot")
    print("="*60)
    print("Type 'quit' to exit, 'clear' to clear history, 'history' to see conversation")
    print("="*60 + "\n")

    # Create chatbot with a system message
    bot = SimpleChatbot(
        system_message="You are a friendly and helpful assistant."
    )

    while True:
        # Get user input
        user_input = input("You: ").strip()

        # Handle commands
        if user_input.lower() == 'quit':
            print("Goodbye! 👋")
            break

        if user_input.lower() == 'clear':
            bot.clear_history()
            print("Conversation history cleared.\n")
            continue

        if user_input.lower() == 'history':
            print("\nConversation History:")
            print("-" * 40)
            for msg in bot.get_history():
                role = msg['role'].capitalize()
                content = msg['content']
                print(f"{role}: {content}")
            print("-" * 40 + "\n")
            continue

        if not user_input:
            continue

        # Get and print response
        response = bot.chat(user_input)
        print(f"Assistant: {response}\n")

if __name__ == "__main__":
    main()
```

### Chatbot Features

This simple chatbot includes:
- ✅ Conversation history maintenance
- ✅ System message for personality
- ✅ Error handling
- ✅ Clear history functionality
- ✅ View conversation history

---

## Token Usage and Pricing

### Understanding Tokens

**Tokens** are pieces of words. OpenAI models process and generate text in tokens.

**Rule of thumb**:
- 1 token ≈ 4 characters in English
- 1 token ≈ ¾ of a word
- 100 tokens ≈ 75 words

**Examples**:
```
"ChatGPT is great!" = 5 tokens
"Hello, how are you?" = 6 tokens
"The quick brown fox" = 4 tokens
```

### Token Calculation Example

```python
"""
07_token_usage.py - Understanding and tracking token usage
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

def estimate_cost(tokens, model="gpt-3.5-turbo"):
    """Estimate cost based on token usage"""
    # Pricing (as of 2024 - check current pricing)
    pricing = {
        "gpt-3.5-turbo": {
            "input": 0.0005 / 1000,   # $0.50 per 1M input tokens
            "output": 0.0015 / 1000    # $1.50 per 1M output tokens
        },
        "gpt-4": {
            "input": 0.03 / 1000,      # $30 per 1M input tokens
            "output": 0.06 / 1000      # $60 per 1M output tokens
        }
    }

    if model not in pricing:
        return "Unknown model"

    return pricing[model]

def analyze_request(prompt, model="gpt-3.5-turbo"):
    """Make a request and analyze token usage"""
    print(f"\nAnalyzing request with model: {model}")
    print("-" * 60)

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )

    usage = response.usage
    pricing = estimate_cost(0, model)

    print(f"Prompt: {prompt[:50]}...")
    print(f"\nToken Usage:")
    print(f"  Input tokens:  {usage.prompt_tokens}")
    print(f"  Output tokens: {usage.completion_tokens}")
    print(f"  Total tokens:  {usage.total_tokens}")

    # Calculate cost
    input_cost = usage.prompt_tokens * pricing["input"]
    output_cost = usage.completion_tokens * pricing["output"]
    total_cost = input_cost + output_cost

    print(f"\nEstimated Cost:")
    print(f"  Input:  ${input_cost:.6f}")
    print(f"  Output: ${output_cost:.6f}")
    print(f"  Total:  ${total_cost:.6f}")

    print(f"\nResponse: {response.choices[0].message.content}")

def main():
    print("="*60)
    print("Token Usage and Cost Analysis")
    print("="*60)

    # Short prompt
    analyze_request(
        "Say hello!",
        "gpt-3.5-turbo"
    )

    # Longer prompt
    analyze_request(
        "Write a detailed paragraph explaining what machine learning is.",
        "gpt-3.5-turbo"
    )

if __name__ == "__main__":
    main()
```

### Cost Optimization Tips

1. **Use appropriate models**: Don't use GPT-4 when GPT-3.5-turbo suffices
2. **Set max_tokens**: Limit response length
3. **Trim conversation history**: Don't send entire history every time
4. **Cache responses**: Store and reuse common responses
5. **Batch requests**: Group similar requests when possible

---

## Exercises

### Exercise 1: Personality Bot
Create a chatbot with a specific personality (e.g., Shakespeare, a detective, a chef). Use system messages to set the personality.

### Exercise 2: Token Counter
Build a script that:
1. Takes user input
2. Makes an API request
3. Shows before and after token counts
4. Calculates the cost
5. Tracks cumulative usage

### Exercise 3: Temperature Explorer
Create a script that generates the same prompt with different temperature values (0.0, 0.5, 1.0, 1.5, 2.0) and compares the outputs.

### Exercise 4: Error Simulator
Write a script that intentionally triggers different types of errors and handles them gracefully:
- Invalid API key
- Invalid model name
- Rate limiting (make rapid requests)

### Exercise 5: Multi-Model Chatbot
Build a chatbot that lets users switch between GPT-3.5 and GPT-4 mid-conversation.

---

## Summary

### Key Takeaways

✅ **What We Learned**:
- How to make basic API requests with the chat completions endpoint
- Different models and when to use each one
- Request parameters that control model behavior
- Response structure and how to extract information
- Proper error handling with retries
- Building an interactive chatbot with conversation history
- Token usage and cost implications

✅ **Skills Acquired**:
- Making OpenAI API calls
- Working with different models
- Implementing error handling
- Managing conversation state
- Tracking token usage
- Building simple AI applications

### Best Practices Recap

1. ✅ Always handle errors with try-except
2. ✅ Implement retry logic for transient failures
3. ✅ Use appropriate models for your use case
4. ✅ Track token usage to manage costs
5. ✅ Set max_tokens to control response length
6. ✅ Use system messages to guide behavior
7. ✅ Maintain conversation history for context

### Next Steps

In **Module 3: Core Concepts**, you'll dive deeper into:
- Advanced text generation techniques
- Code generation with Codex
- Vision and image analysis
- Audio and speech processing
- Structured outputs
- Function calling

---

## Additional Resources

- 📚 [Chat Completions API Reference](https://platform.openai.com/docs/api-reference/chat)
- 📖 [Models Documentation](https://platform.openai.com/docs/models)
- 💬 [Pricing](https://openai.com/pricing)
- 🎓 [OpenAI Cookbook - How to format inputs](https://github.com/openai/openai-cookbook)

---

## Knowledge Check

1. What are the three roles in chat messages?
2. What does the `temperature` parameter control?
3. How do you calculate the total cost of an API request?
4. What is the difference between GPT-4 and GPT-3.5-turbo?
5. What is exponential backoff and why is it useful?
6. How many tokens are approximately in "Hello, world!"?

**Answers**:
1. system, user, assistant
2. Randomness/creativity of responses (0=focused, 2=creative)
3. (input_tokens × input_price) + (output_tokens × output_price)
4. GPT-4 is more capable but slower and more expensive
5. Increasing wait time between retries; helps with rate limiting
6. Approximately 4 tokens

---

[⬅️ Previous: Module 1](../module-01-introduction/README.md) | [Home](../README.md) | [Next: Module 3 ➡️](../module-03-core-concepts/README.md)
