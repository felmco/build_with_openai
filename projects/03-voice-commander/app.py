"""
Project 3: Voice Ops Commander
------------------------------
A voice-controlled assistant that can execute system commands.
Demonstrates Speech-to-Text (Whisper), Text-to-Speech (TTS), and Function Calling.
"""

import os
import json
import subprocess
import time
from typing import Optional

# Audio libraries
# pip install sounddevice numpy scipy
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav

from openai import OpenAI

client = OpenAI()

# --- Config ---
SAMPLE_RATE = 44100  # Hertz
RECORDING_FILE = "input_command.wav"
RESPONSE_FILE = "response.mp3"

# --- System Functions ---

def open_application(app_name: str):
    """Opens a system application (Windows specific example)"""
    print(f"🖥️  System executing: Open {app_name}")
    try:
        if "notepad" in app_name.lower():
            subprocess.Popen("notepad.exe")
            return "Opened Notepad successfully."
        elif "calc" in app_name.lower():
            subprocess.Popen("calc.exe")
            return "Opened Calculator successfully."
        elif "browser" in app_name.lower() or "chrome" in app_name.lower():
            subprocess.Popen("start chrome", shell=True) # Assumes Chrome is in path
            return "Opened Web Browser."
        else:
            return f"I don't know how to open {app_name} yet."
    except Exception as e:
        return f"Failed to open {app_name}: {str(e)}"

def get_system_time():
    """Returns current system time"""
    return time.strftime("%I:%M %p")

# Tool definitions for GPT
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "open_application",
            "description": "Opens a desktop application on the user's computer",
            "parameters": {
                "type": "object",
                "properties": {
                    "app_name": {"type": "string", "description": "The name of the application"}
                },
                "required": ["app_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_system_time",
            "description": "Get the current time",
            "parameters": {"type": "object", "properties": {}}
        }
    }
]

# --- Audio Functions ---

def record_audio(duration=5):
    """Simple audio recorder (fixed duration for demo)"""
    print(f"🎤 Recording for {duration} seconds... Speak now!")
    audio_data = sd.rec(int(duration * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1)
    sd.wait()  # Wait until recording is finished
    
    # Save as WAV
    # Normalize to 16-bit PCM
    audio_data_int16 = (audio_data * 32767).astype(np.int16)
    wav.write(RECORDING_FILE, SAMPLE_RATE, audio_data_int16)
    print("✅ Recording saved.")

def speak_response(text):
    """Generate and play speech"""
    print(f"🗣️  Speaking: {text}")
    
    response = client.audio.speech.create(
        model="tts-1",
        voice="onyx",
        input=text
    )
    
    # Save to file
    response.stream_to_file(RESPONSE_FILE)
    
    # Play file (Windows specific)
    os.system(f"start {RESPONSE_FILE}")

# --- Main Logic ---

def process_command():
    # 1. Transcribe
    print("📝 Transcribing audio...")
    with open(RECORDING_FILE, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file
        )
    user_text = transcription.text
    print(f"👤 User said: '{user_text}'")
    
    # 2. Think & Act (GPT-4o)
    messages = [
        {"role": "system", "content": "You are a helpful voice assistant. Keep responses short and conversational suitable for voice output."},
        {"role": "user", "content": user_text}
    ]
    
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=TOOLS,
        tool_choice="auto"
    )
    
    response_message = completion.choices[0].message
    tool_calls = response_message.tool_calls
    
    final_response_text = ""
    
    if tool_calls:
        # 3. Execute Tool
        messages.append(response_message)
        
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            function_response = ""
            
            if function_name == "open_application":
                function_response = open_application(function_args.get("app_name"))
            elif function_name == "get_system_time":
                function_response = get_system_time()
                
            messages.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": function_response,
            })
            
        # 4. Get Final Answer
        second_response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )
        final_response_text = second_response.choices[0].message.content
        
    else:
        # No tool needed, just chat
        final_response_text = response_message.content
        
    return final_response_text

def main():
    print("🎙️ VOICE OPS COMMANDER")
    print("="*60)
    print("Press Enter to start recording (5 seconds max)...")
    input()
    
    try:
        record_audio(duration=4)
        print("Processing...")
        response_text = process_command()
        speak_response(response_text)
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nNote: This script requires a microphone and audio libraries installed.")

if __name__ == "__main__":
    main()
