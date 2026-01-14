# 🎙️ Project 3: Voice Ops Commander

## 📝 Overview

In this advanced project, we build a **Voice-Controlled interface** for your computer. This mimics experiences like Jarvis or Star Trek computers.

We combine two powerful OpenAI Audio APIs:
1.  **Whisper (Speech-to-Text)**: To listen to your voice commands.
2.  **TTS-1 (Text-to-Speech)**: To speak back the results.
3.  **GPT-4o**: To understand the intent of your command and decide what action to take.

### Key Concepts
- **Audio Pipelines**: Recording -> Transcribing -> Processing -> Speaking.
- **Function Calling**: Mapping natural language ("Open the calculator") to actual code functions (`subprocess.Popen`).
- **Real-time Interaction**: Minimizing latency for a smooth feel.

---

## 🏗️ Step-by-Step Implementation

### Step 1: Handling Audio Input

We need a way to record audio. In Python, we can use `sounddevice` and `numpy`.
*Note: This requires a microphone.*

```python
import sounddevice as sd
import numpy as np
# ... recording logic ...
```

### Step 2: The Action System (Function Calling)

We define what our computer can *do*.

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "open_application",
            "description": "Opens a desktop application",
            "parameters": {
                "type": "object",
                "properties": {
                    "app_name": {"type": "string", "description": "Name of the app (e.g., 'notepad', 'calculator')"}
                },
                "required": ["app_name"]
            }
        }
    }
]
```

### Step 3: The Brain (GPT-4o)

We send the transcribed text to GPT-4o with our tools defined. If GPT-4o tells us to run a tool, we execute it using Python's `subprocess`.

### Step 4: The Voice (TTS)

Finally, we generate a spoken response confirming the action.

```python
response = client.audio.speech.create(
    model="tts-1",
    voice="onyx",
    input="Opening calculator now."
)
response.stream_to_file("output.mp3")
```

---

## 💻 The Code

The complete code is available in `app.py`.

### How to Run

1.  **Prerequisites**: You need `ffmpeg` installed on your system for audio processing.
2.  Install requirements:
    ```bash
    pip install openai sounddevice numpy scipy
    ```
3.  Run the commander:
    ```bash
    python app.py
    ```
4.  Press **Enter** to start recording, speak your command (e.g., "Open Notepad"), and press **Enter** to stop.

### Expected Behavior

1.  **User**: "Open Notepad and tell me a joke."
2.  **Agent**: "Opening Notepad..." (Notepad opens) "Why did the developer go broke? Because he used up all his cache." (Spoken aloud)

---

## 🧠 Challenge for You

**Extend this project**:
1.  **Wake Word Detection**: Add a library like `Porcupine` to listen for "Hey Computer" instead of pressing Enter.
2.  **System Info**: Add a function to read back CPU usage or Battery status.
