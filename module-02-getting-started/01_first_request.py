"""
01_first_request.py - Your first OpenAI API call

This script demonstrates the simplest way to interact with the OpenAI API.
Run this after completing Module 1 setup.
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client
# The API key is automatically read from OPENAI_API_KEY environment variable
client = OpenAI()


def main():
    print("Making your first API request...\n")

    # Make the API call
    response = client.chat.completions.create(
        model="gpt-5-mini",  # The model to use
        messages=[
            {"role": "user", "content": "Hello! Can you introduce yourself in one sentence?"}
        ]
    )

    # Extract and print the response
    assistant_message = response.choices[0].message.content
    print("Assistant:", assistant_message)
    print("\nSuccess! You've made your first API call! 🎉")


if __name__ == "__main__":
    main()
