"""
01_advanced_prompting.py - Advanced techniques
"""

from openai import OpenAI

client = OpenAI()

def chain_of_thought_demo(question):
    print(f"\n❓ Question: {question}")
    
    # Standard Prompt
    print("--- Standard ---")
    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[{"role": "user", "content": question}]
    )
    print(response.choices[0].message.content)
    
    # CoT Prompt
    print("\n--- Chain of Thought ---")
    cot_prompt = f"{question}\nLet's think step by step."
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": cot_prompt}]
    )
    print(response.choices[0].message.content)

def few_shot_demo():
    print("\n--- Few Shot ---")
    messages = [
        {"role": "system", "content": "Convert standard English to Pirate speak."},
        {"role": "user", "content": "Hello friend."},
        {"role": "assistant", "content": "Ahoy matey!"},
        {"role": "user", "content": "Where is the bathroom?"},
        {"role": "assistant", "content": "Avast! Where be the head?"},
        {"role": "user", "content": "I am hungry."}
    ]
    response = client.chat.completions.create(
        model="gpt-5-mini", messages=messages
    )
    print(f"I am hungry -> {response.choices[0].message.content}")

def main():
    print("🧠 ADVANCED PROMPTING")
    
    chain_of_thought_demo("If I have 3 apples, eat 1, and buy 2 more, how many do I have?")
    few_shot_demo()

if __name__ == "__main__":
    main()
