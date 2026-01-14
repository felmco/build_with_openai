"""
06_simple_chatbot.py - A simple interactive chatbot

This chatbot maintains conversation history and allows multi-turn conversations.
Features:
- Conversation history
- System message for personality
- Commands: quit, clear, history
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()


class SimpleChatbot:
    """A simple chatbot that maintains conversation history"""

    def __init__(self, system_message=None):
        """Initialize the chatbot with optional system message"""
        self.messages = []

        if system_message:
            self.messages.append({
                "role": "system",
                "content": system_message
            })

    def chat(self, user_message):
        """Send a message and get a response"""
        # Add user message to history
        self.messages.append({
            "role": "user",
            "content": user_message
        })

        try:
            # Get response from OpenAI
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=self.messages,
                temperature=0.7
            )

            # Extract assistant's response
            assistant_message = response.choices[0].message.content

            # Add assistant response to history
            self.messages.append({
                "role": "assistant",
                "content": assistant_message
            })

            return assistant_message

        except Exception as e:
            return f"Error: {str(e)}"

    def get_history(self):
        """Get the conversation history"""
        return self.messages

    def clear_history(self):
        """Clear conversation history (keeps system message if set)"""
        system_messages = [msg for msg in self.messages if msg["role"] == "system"]
        self.messages = system_messages


def main():
    """Run the interactive chatbot"""
    print("="*60)
    print("Simple Chatbot")
    print("="*60)
    print("Type 'quit' to exit, 'clear' to clear history, 'history' to see conversation")
    print("="*60 + "\n")

    # Create chatbot with a system message
    bot = SimpleChatbot(
        system_message="You are a friendly and helpful assistant."
    )

    while True:
        # Get user input
        user_input = input("You: ").strip()

        # Handle commands
        if user_input.lower() == 'quit':
            print("Goodbye!")
            break

        if user_input.lower() == 'clear':
            bot.clear_history()
            print("Conversation history cleared.\n")
            continue

        if user_input.lower() == 'history':
            print("\nConversation History:")
            print("-" * 40)
            for msg in bot.get_history():
                role = msg['role'].capitalize()
                content = msg['content']
                print(f"{role}: {content}")
            print("-" * 40 + "\n")
            continue

        if not user_input:
            continue

        # Get and print response
        response = bot.chat(user_input)
        print(f"Assistant: {response}\n")


if __name__ == "__main__":
    main()
