"""
03_cost_estimator.py - Token calculation
"""

import tiktoken

def count_tokens(text, model="gpt-4o"):
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    
    return len(encoding.encode(text))

def calculator_demo():
    print("💰 COST ESTIMATOR")
    
    prompt = """
    This is a long legal document that needs summarization. 
    It represents a typical heavy payload for an enterprise application.
    """ * 50
    
    tokens = count_tokens(prompt)
    print(f"Input Tokens: {tokens}")
    
    # 2026 Simulated Pricing (per 1M tokens)
    prices = {
        "gpt-5-mini": 0.15,
        "gpt-4o": 2.50,
        "o1-preview": 15.00
    }
    
    print("\nEstimated Cost for this prompt:")
    for model, price in prices.items():
        cost = (tokens / 1_000_000) * price
        print(f"  {model.ljust(12)}: ${cost:.6f}")

if __name__ == "__main__":
    calculator_demo()
