"""
01_streaming.py - Implementing streaming responses
"""

import sys
import time
from openai import OpenAI

client = OpenAI()

def chat_stream(prompt):
    print(f"\nUser: {prompt}\nAgent: ", end="", flush=True)
    
    stream = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[{"role": "user", "content": prompt}],
        stream=True
    )
    
    # Iterate through the stream of events
    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:
            print(content, end="", flush=True)
            # Simulate a UI update delay if needed (usually not)
            # time.sleep(0.01) 
    print() # Newline at end

def main():
    print("🌊 STREAMING DEMO")
    print("="*60)
    
    chat_stream("Write a short poem about the speed of light.")
    chat_stream("Explain quantum entanglement in 2 sentences.")

if __name__ == "__main__":
    main()
