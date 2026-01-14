"""
04_response_structure.py - Inspect the full API response
"""

import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()


def main():
    print("Inspecting full response structure...")

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {"role": "user", "content": "Hello!"}
        ]
    )

    # Convert response to dictionary and pretty print
    # Note: dict() might not work on the pydantic object directly in v1.x, 
    # use model_dump() if available or inspect attributes
    
    print("\nFull Response Object:")
    try:
        # Pydantic v2 style (used in newer OpenAI SDKs)
        print(json.dumps(response.model_dump(), indent=2))
    except AttributeError:
        # Fallback or just print object
        print(response)

    print("\nKey Attributes:")
    print(f"ID: {response.id}")
    print(f"Model: {response.model}")
    print(f"Created: {response.created}")
    print(f"Usage: {response.usage}")
    print(f"Finish Reason: {response.choices[0].finish_reason}")
    print(f"Content: {response.choices[0].message.content}")


if __name__ == "__main__":
    main()
