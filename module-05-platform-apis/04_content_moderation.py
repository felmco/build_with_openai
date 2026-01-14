"""
04_content_moderation.py - Implement content moderation
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()


def moderate_content(text):
    """Moderate content for safety"""
    print(f"\n🔍 Moderating content...")

    response = client.moderations.create(input=text)
    result = response.results[0]

    print(f"\nFlagged: {result.flagged}")

    if result.flagged:
        print("\nCategory scores:")
        for category, score in result.category_scores.model_dump().items():
            if score > 0.01:  # Show significant scores
                print(f"  {category}: {score:.4f}")

    return result


def safe_chat_completion(user_input):
    """Chat completion with content moderation"""
    print("\n💬 Processing chat with moderation...")

    # Moderate user input
    moderation = moderate_content(user_input)

    if moderation.flagged:
        return "I cannot process this request as it violates our content policy."

    # Safe to proceed
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_input}]
    )

    assistant_response = response.choices[0].message.content

    # Moderate assistant output (optional)
    output_moderation = moderate_content(assistant_response)

    if output_moderation.flagged:
        return "I apologize, but I cannot provide that response."

    return assistant_response


moderation_guide = """
CONTENT MODERATION GUIDE:

Categories:
- hate: Hateful content
- hate/threatening: Hateful with violence
- harassment: Harassing content
- harassment/threatening: Harassment with threats
- self-harm: Self-harm related
- self-harm/intent: Self-harm intent
- self-harm/instructions: Self-harm instructions
- sexual: Sexual content
- sexual/minors: Sexual content with minors
- violence: Violent content
- violence/graphic: Graphic violence

Best Practices:
1. Moderate user input before processing
2. Moderate AI output before showing users
3. Set appropriate thresholds
4. Log moderation events
5. Provide clear feedback to users

Implementation Pattern:
1. Receive user input
2. Run moderation check
3. If flagged, reject request
4. If safe, process with AI
5. Moderate AI response
6. Return to user

Use Cases:
- User-generated content platforms
- Chat applications
- Content creation tools
- Community platforms
"""

print(moderation_guide)


if __name__ == "__main__":
    # Test moderation
    safe_content = "Tell me about the weather"
    moderate_content(safe_content)

    unsafe_content = "I hate everyone and want to cause harm"
    moderate_content(unsafe_content)
