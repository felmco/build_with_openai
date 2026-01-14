"""
03_code_generation.py - Generate code from natural language descriptions
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()


def generate_function(description, language="Python"):
    """Generate a function from a description"""
    print("\n" + "="*60)
    print(f"GENERATING {language.upper()} FUNCTION")
    print("="*60)
    print(f"Description: {description}\n")

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {
                "role": "system",
                "content": f"You are an expert {language} programmer. Generate clean, well-documented code."
            },
            {
                "role": "user",
                "content": f"Write a {language} function that {description}. Include docstring and comments."
            }
        ],
        temperature=0.2  # Lower temperature for more consistent code
    )

    code = response.choices[0].message.content
    print(code)
    return code


def explain_code(code):
    """Explain what a piece of code does"""
    print("\n" + "="*60)
    print("CODE EXPLANATION")
    print("="*60)

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[{
            "role": "user",
            "content": f"Explain what this code does line by line:\n\n```python\n{code}\n```"
        }]
    )

    print(response.choices[0].message.content)


def debug_code(buggy_code):
    """Find and fix bugs in code"""
    print("\n" + "="*60)
    print("CODE DEBUGGING")
    print("="*60)

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[{
            "role": "user",
            "content": f"""Find and fix the bugs in this code. Explain what was wrong and provide the corrected version:

```python
{buggy_code}
```"""
        }]
    )

    print(response.choices[0].message.content)


def refactor_code(code):
    """Improve code quality"""
    print("\n" + "="*60)
    print("CODE REFACTORING")
    print("="*60)

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[{
            "role": "user",
            "content": f"""Refactor this code to improve readability, efficiency, and follow best practices:

```python
{code}
```"""
        }]
    )

    print(response.choices[0].message.content)


def main():
    print("Code Generation Examples")

    # Example 1: Generate a function
    generate_function("calculates the factorial of a number using recursion")

    # Example 2: Generate a class
    generate_function("creates a BankAccount class with deposit and withdraw methods")

    # Example 3: Explain code
    sample_code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
"""
    explain_code(sample_code.strip())

    # Example 4: Debug code
    buggy = """
def calculate_average(numbers):
    total = 0
    for num in numbers:
        total += num
    return total / len(number)
"""
    debug_code(buggy.strip())


if __name__ == "__main__":
    main()
