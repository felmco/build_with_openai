"""
08_text_to_speech.py - Generate speech from text
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()


def generate_speech(text, voice="alloy", model="tts-1", output_file="speech.mp3"):
    """Generate speech from text"""
    print("\n" + "="*60)
    print("GENERATING SPEECH")
    print("="*60)
    print(f"Text: {text[:100]}...")
    print(f"Voice: {voice}, Model: {model}\n")

    response = client.audio.speech.create(
        model=model,  # "tts-1" or "tts-1-hd"
        voice=voice,   # alloy, echo, fable, onyx, nova, shimmer
        input=text
    )

    # Save to file
    speech_file_path = Path(output_file)
    response.stream_to_file(speech_file_path)

    print(f"Speech saved to: {speech_file_path}")
    return speech_file_path


def demonstrate_voices():
    """Generate samples with different voices"""
    print("\n" + "="*60)
    print("COMPARING DIFFERENT VOICES")
    print("="*60)

    text = "Hello! I'm an AI assistant powered by OpenAI. How can I help you today?"
    voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]

    for voice in voices:
        output_file = f"voice_sample_{voice}.mp3"
        generate_speech(text, voice=voice, output_file=output_file)


def main():
    print("Text-to-Speech Generation")

    # Example 1: Basic TTS
    sample_text = "Welcome to the OpenAI Text-to-Speech API. This is a demonstration of high-quality voice synthesis."
    generate_speech(sample_text, voice="nova", model="tts-1")

    # Example 2: HD quality
    generate_speech(sample_text, voice="nova", model="tts-1-hd", output_file="speech_hd.mp3")

    print("\n" + "="*60)
    print("TTS FEATURES AND BEST PRACTICES")
    print("="*60)
    print("""
Available Voices:
- alloy: Neutral and balanced
- echo: Male, clear and direct
- fable: British accent, warm
- onyx: Deep male voice
- nova: Female, energetic
- shimmer: Female, calm and soothing

Models:
- tts-1: Standard quality, faster, lower cost
- tts-1-hd: High definition, better quality

Best Practices:
1. Choose appropriate voice for your use case
2. Use tts-1 for real-time applications
3. Use tts-1-hd for content where quality matters
4. Break long text into smaller chunks
5. Test different voices to find the best fit

Supported input: Up to 4096 characters per request
Output format: MP3 by default
    """)


if __name__ == "__main__":
    main()
