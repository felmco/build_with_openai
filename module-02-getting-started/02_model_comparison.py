"""
02_model_comparison.py - Compare different OpenAI models
"""

import os
import time
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()


def test_model(model_name, prompt):
    """Test a specific model and measure response time"""
    print(f"\nTesting model: {model_name}")
    start_time = time.time()
    
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100
        )
        
        duration = time.time() - start_time
        content = response.choices[0].message.content
        
        print(f"Time: {duration:.2f} seconds")
        print(f"Response: {content[:100]}...")
        return duration
    except Exception as e:
        print(f"Error: {e}")
        return 0


def main():
    prompt = "Explain the concept of recursion in programming in one paragraph."
    print(f"Prompt: {prompt}")
    print("Comparing model responses...")

    # Test different models
    models = ["gpt-5-mini", "gpt-5.2", "o1"]

    for model in models:
        test_model(model, prompt)


if __name__ == "__main__":
    main()
