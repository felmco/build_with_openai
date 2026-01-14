"""
08_structured_outputs.py - Generate structured JSON data
"""

import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()


def generate_json_mode(prompt):
    """Generate JSON using JSON mode"""
    print("\n" + "="*60)
    print("JSON MODE")
    print("="*60)

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that outputs in JSON."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        response_format={"type": "json_object"}
    )

    content = response.choices[0].message.content
    print(content)
    
    # Parse to verify validity
    try:
        data = json.loads(content)
        print("\nValid JSON parsed successfully!")
        return data
    except params:
        print("\nError parsing JSON")
        return None


def generate_structured_output_cfg(prompt):
    """Generate structured output with Context-Free Grammar (Pseudo-code for 2026 feature)"""
    print("\n" + "="*60)
    print("STRUCTURED OUTPUT (CFG)")
    print("="*60)
    
    # Schema for a Calendar Event (example)
    schema = {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "time": {"type": "string"},
            "attendees": {"type": "array", "items": {"type": "string"}}
        },
        "required": ["title", "time"]
    }

    # In 2026, this might be handled via a 'response_schema' or similar advanced param
    # For now, we simulate the standard function calling or json schema approach
    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {"role": "system", "content": "Extract event details."},
            {"role": "user", "content": prompt}
        ],
        response_format={
            "type": "json_schema", 
            "json_schema": {
                "name": "event_schema",
                "schema": schema,
                "strict": True
            }
        }
    )
    
    print(response.choices[0].message.content)


def main():
    print("Structured Outputs")

    # Example 1: JSON Mode
    prompt = "Generate a user profile for John Doe, age 30, occupation software engineer"
    generate_json_mode(prompt)

    # Example 2: Structured Output
    # generate_structured_output_cfg("Meeting with the team at 2 PM with Alice and Bob")


if __name__ == "__main__":
    main()
