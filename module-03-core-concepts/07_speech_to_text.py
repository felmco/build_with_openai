"""
07_speech_to_text.py - Transcribe audio with Whisper
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()


def transcribe_audio(audio_file_path):
    """Transcribe audio to text"""
    print("\n" + "="*60)
    print("TRANSCRIBING AUDIO")
    print("="*60)

    with open(audio_file_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="text"
        )

    print(f"Transcript: {transcript}")
    return transcript


def translate_audio(audio_file_path):
    """Translate audio to English"""
    print("\n" + "="*60)
    print("TRANSLATING AUDIO TO ENGLISH")
    print("="*60)

    with open(audio_file_path, "rb") as audio_file:
        translation = client.audio.translations.create(
            model="whisper-1",
            file=audio_file
        )

    print(f"Translation: {translation.text}")
    return translation.text


def text_to_speech(text, output_file="speech.mp3"):
    """Convert text to speech"""
    print("\n" + "="*60)
    print("TEXT TO SPEECH")
    print("="*60)
    print(f"Text: {text}")

    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text
    )

    response.stream_to_file(output_file)
    print(f"Audio saved to: {output_file}")


def main():
    print("Audio and Speech Examples")

    text = "Hello! This is a test of the OpenAI text-to-speech API. It sounds pretty natural, doesn't it?"
    
    # 1. Generate speech
    text_to_speech(text, "test_output.mp3")

    # 2. Transcribe it back (if file exists)
    if os.path.exists("test_output.mp3"):
        transcribe_audio("test_output.mp3")


if __name__ == "__main__":
    main()
