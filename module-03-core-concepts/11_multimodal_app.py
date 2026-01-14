"""
11_multimodal_app.py - Build applications combining multiple modalities
"""

import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()


class MultiModalAssistant:
    """An assistant that can handle text, images, and function calls"""

    def __init__(self):
        self.conversation_history = []

    def process_text(self, user_input):
        """Process text input"""
        self.conversation_history.append({
            "role": "user",
            "content": user_input
        })

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.conversation_history
        )

        assistant_message = response.choices[0].message.content
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })

        return assistant_message

    def process_image_and_text(self, image_url, question):
        """Process image with text question"""
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": question},
                        {"type": "image_url", "image_url": {"url": image_url}}
                    ]
                }
            ]
        )

        return response.choices[0].message.content

    def transcribe_and_analyze(self, audio_file_path):
        """Transcribe audio and analyze the content"""
        # Step 1: Transcribe audio
        with open(audio_file_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )

        transcribed_text = transcript.text

        # Step 2: Analyze the transcribed text
        analysis = self.process_text(
            f"Analyze this transcript and provide key points: {transcribed_text}"
        )

        return {
            "transcript": transcribed_text,
            "analysis": analysis
        }


def main():
    print("Multi-Modal Applications")

    assistant = MultiModalAssistant()

    print("\n" + "="*60)
    print("MULTI-MODAL CAPABILITIES")
    print("="*60)
    print("""
Combining Modalities:

1. Text + Vision:
   - Describe images and answer questions
   - Analyze documents with text and images
   - Visual question answering

2. Text + Audio:
   - Transcribe audio and analyze content
   - Generate speech from text responses
   - Voice-controlled applications

3. Text + Functions:
   - Chat interfaces with tool use
   - Agents that can take actions
   - Data retrieval and processing

4. All Together:
   - Transcribe audio → analyze with AI → generate speech response
   - Analyze image → extract data → call functions → respond
   - Multi-step workflows with different modalities

Example Multi-Modal Workflows:

Workflow 1: Meeting Assistant
- Transcribe meeting audio (Speech-to-Text)
- Extract action items (Text Processing + Structured Output)
- Send notifications (Function Calling)
- Generate summary report (Text Generation)

Workflow 2: Visual Product Search
- User uploads product image (Vision)
- Extract product details (Vision + Structured Output)
- Search database (Function Calling)
- Provide recommendations (Text Generation)

Workflow 3: Content Creation Pipeline
- Generate article outline (Text Generation)
- Create accompanying images (DALL-E)
- Generate audio narration (Text-to-Speech)
- Combine into complete content package
    """)


if __name__ == "__main__":
    main()
