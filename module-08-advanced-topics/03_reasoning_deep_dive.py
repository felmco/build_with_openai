"""
03_reasoning_deep_dive.py - Using o1 models
"""

import time
from openai import OpenAI

client = OpenAI()

def solve_complex_problem():
    print("🤔 Using o1 for complex reasoning...")
    
    # A classic logic puzzle or coding challenge
    problem = """
    Write a Python script that calculates the first 100 prime numbers. 
    Then, find the sum of these numbers. 
    Explain the algorithm efficiency (Big O).
    """
    
    start_time = time.time()
    
    response = client.chat.completions.create(
        model="o1-preview", # or o1-mini for speed
        messages=[
            {"role": "user", "content": problem}
        ],
        # reasoning_effort="high" # If available in your API version
    )
    
    duration = time.time() - start_time
    content = response.choices[0].message.content
    
    print(f"✅ Solution generated in {duration:.2f}s")
    print("\n--- Output ---")
    print(content[:500] + "...\n(truncated)")

def main():
    print("🧠 REASONING (o1) DEMO")
    print("="*60)
    solve_complex_problem()

if __name__ == "__main__":
    main()
