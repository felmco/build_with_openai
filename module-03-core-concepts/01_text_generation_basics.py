"""
01_text_generation_basics.py - Advanced text generation techniques
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()


def zero_shot_example():
    """Zero-shot: Task without examples"""
    print("\n" + "="*60)
    print("ZERO-SHOT PROMPTING")
    print("="*60)

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[{
            "role": "user",
            "content": "Classify the sentiment of this text as positive, negative, or neutral: 'I love this product!'"
        }]
    )

    print(response.choices[0].message.content)


def few_shot_example():
    """Few-shot: Provide examples to guide the model"""
    print("\n" + "="*60)
    print("FEW-SHOT PROMPTING")
    print("="*60)

    prompt = """Classify the sentiment as positive, negative, or neutral.

Examples:
Text: "This is amazing!" -> Sentiment: positive
Text: "I hate waiting in line." -> Sentiment: negative
Text: "The sky is blue." -> Sentiment: neutral

Now classify this:
Text: "This product exceeded my expectations!" -> Sentiment:"""

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    print(response.choices[0].message.content)


def chain_of_thought():
    """Chain-of-thought: Encourage step-by-step reasoning"""
    print("\n" + "="*60)
    print("CHAIN-OF-THOUGHT PROMPTING")
    print("="*60)

    prompt = """Solve this problem step by step:

Question: If a train travels 120 miles in 2 hours, how far will it travel in 5 hours at the same speed?

Let's think through this step-by-step:"""

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    print(response.choices[0].message.content)


def role_prompting():
    """Role prompting: Assign a specific role/persona"""
    print("\n" + "="*60)
    print("ROLE PROMPTING")
    print("="*60)

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {
                "role": "system",
                "content": "You are an expert Python developer with 10 years of experience. Explain concepts clearly and provide best practices."
            },
            {
                "role": "user",
                "content": "What's the difference between a list and a tuple in Python?"
            }
        ]
    )

    print(response.choices[0].message.content)


def main():
    print("Advanced Text Generation Techniques")

    zero_shot_example()
    few_shot_example()
    chain_of_thought()
    role_prompting()


if __name__ == "__main__":
    main()
