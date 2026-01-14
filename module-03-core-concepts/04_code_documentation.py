"""
04_code_documentation.py - Generate documentation and tests for code
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()


def generate_docstring(function_code):
    """Generate comprehensive docstring for a function"""
    print("\n" + "="*60)
    print("GENERATING DOCSTRING")
    print("="*60)

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[{
            "role": "user",
            "content": f"""Generate a comprehensive docstring for this function following PEP 257 and Google style guide:

```python
{function_code}
```

Include:
- Brief description
- Args with types
- Returns with type
- Raises (if applicable)
- Example usage"""
        }]
    )

    print(response.choices[0].message.content)


def generate_unit_tests(function_code):
    """Generate unit tests for a function"""
    print("\n" + "="*60)
    print("GENERATING UNIT TESTS")
    print("="*60)

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[{
            "role": "user",
            "content": f"""Generate comprehensive pytest unit tests for this function:

```python
{function_code}
```

Include:
- Normal cases
- Edge cases
- Error cases
- Multiple test methods"""
        }]
    )

    print(response.choices[0].message.content)


def main():
    sample_function = """
def calculate_bmi(weight_kg, height_m):
    return weight_kg / (height_m ** 2)
"""

    generate_docstring(sample_function.strip())
    generate_unit_tests(sample_function.strip())


if __name__ == "__main__":
    main()
