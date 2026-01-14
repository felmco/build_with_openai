"""
03_parameters_demo.py - Experiment with API parameters
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()


def demonstrate_temperature():
    """Show how temperature affects creativity"""
    print("\n" + "="*60)
    print("TEMPERATURE DEMO")
    print("="*60)
    
    prompt = "Complete this sentence: The best way to start the day is..."
    
    # Low temperature (Deterministic)
    print("\nLow Temperature (0.2) - Focused/Deterministic:")
    for i in range(2):
        response = client.chat.completions.create(
            model="gpt-5-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=50
        )
        print(f"Attempt {i+1}: {response.choices[0].message.content}")

    # High temperature (Creative)
    print("\nHigh Temperature (0.9) - Creative/Random:")
    for i in range(2):
        response = client.chat.completions.create(
            model="gpt-5-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9,
            max_tokens=50
        )
        print(f"Attempt {i+1}: {response.choices[0].message.content}")


def demonstrate_system_message():
    """Show how system messages control behavior"""
    print("\n" + "="*60)
    print("SYSTEM MESSAGE DEMO")
    print("="*60)
    
    user_msg = "Tell me about quantum physics."
    
    # Persona 1: Five year old
    print("\nPersona: Explain to a 5-year-old")
    response1 = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {"role": "system", "content": "You are a kindergarten teacher. Explain things simply."},
            {"role": "user", "content": user_msg}
        ],
        max_tokens=100
    )
    print(response1.choices[0].message.content)
    
    # Persona 2: Professor
    print("\nPersona: PhD Professor")
    response2 = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {"role": "system", "content": "You are a physics professor. Use technical terms."},
            {"role": "user", "content": user_msg}
        ],
        max_tokens=100
    )
    print(response2.choices[0].message.content)


def demonstrate_multiple_completions():
    """Generate multiple choices for one prompt"""
    print("\n" + "="*60)
    print("MULTIPLE COMPLETIONS (parameter n)")
    print("="*60)
    
    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[{"role": "user", "content": "Suggest a name for a coffee shop."}],
        n=3,
        temperature=0.9
    )
    
    print("Suggestions:")
    for i, choice in enumerate(response.choices):
        print(f"{i+1}. {choice.message.content}")


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


def main():
    demonstrate_temperature()
    demonstrate_system_message()
    demonstrate_multiple_completions()
    demonstrate_new_parameters()


if __name__ == "__main__":
    main()
