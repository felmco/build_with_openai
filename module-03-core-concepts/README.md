# Module 3: Core Concepts

## 📋 Module Overview

**Duration**: 3-4 hours
**Level**: Beginner to Intermediate
**Prerequisites**: Modules 1-2 completed

This module covers the fundamental capabilities of the OpenAI platform. You'll learn text generation, code generation, vision/image processing, audio/speech, structured outputs, and function calling.

---

## 🎯 Learning Objectives

By the end of this module, you will be able to:
- ✅ Master advanced text generation techniques
- ✅ Generate and analyze code programmatically
- ✅ Work with images and vision capabilities
- ✅ Process audio with speech-to-text and text-to-speech
- ✅ Generate structured JSON outputs with schemas
- ✅ Implement function calling for tool use
- ✅ Build multi-modal applications

---

## 📖 Table of Contents

1. [Text Generation](#1-text-generation)
2. [Code Generation](#2-code-generation)
3. [Vision and Image Analysis](#3-vision-and-image-analysis)
4. [Audio and Speech](#4-audio-and-speech)
5. [Structured Outputs](#5-structured-outputs)
6. [Function Calling](#6-function-calling)
7. [Multi-Modal Applications](#7-multi-modal-applications)
8. [Exercises](#exercises)
9. [Summary](#summary)

---

## 1. Text Generation

### 1.1 Advanced Prompting Techniques

Text generation is the foundation of working with OpenAI. Let's explore advanced techniques beyond basic prompts.

#### Zero-Shot Prompting

```python
"""
01_text_generation_basics.py - Advanced text generation techniques
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()


def zero_shot_example():
    """Zero-shot: Task without examples"""
    print("\n" + "="*60)
    print("ZERO-SHOT PROMPTING")
    print("="*60)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "user",
            "content": "Classify the sentiment of this text as positive, negative, or neutral: 'I love this product!'"
        }]
    )

    print(response.choices[0].message.content)


def few_shot_example():
    """Few-shot: Provide examples to guide the model"""
    print("\n" + "="*60)
    print("FEW-SHOT PROMPTING")
    print("="*60)

    prompt = """Classify the sentiment as positive, negative, or neutral.

Examples:
Text: "This is amazing!" -> Sentiment: positive
Text: "I hate waiting in line." -> Sentiment: negative
Text: "The sky is blue." -> Sentiment: neutral

Now classify this:
Text: "This product exceeded my expectations!" -> Sentiment:"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    print(response.choices[0].message.content)


def chain_of_thought():
    """Chain-of-thought: Encourage step-by-step reasoning"""
    print("\n" + "="*60)
    print("CHAIN-OF-THOUGHT PROMPTING")
    print("="*60)

    prompt = """Solve this problem step by step:

Question: If a train travels 120 miles in 2 hours, how far will it travel in 5 hours at the same speed?

Let's think through this step-by-step:"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    print(response.choices[0].message.content)


def role_prompting():
    """Role prompting: Assign a specific role/persona"""
    print("\n" + "="*60)
    print("ROLE PROMPTING")
    print("="*60)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are an expert Python developer with 10 years of experience. Explain concepts clearly and provide best practices."
            },
            {
                "role": "user",
                "content": "What's the difference between a list and a tuple in Python?"
            }
        ]
    )

    print(response.choices[0].message.content)


def main():
    print("Advanced Text Generation Techniques")

    zero_shot_example()
    few_shot_example()
    chain_of_thought()
    role_prompting()


if __name__ == "__main__":
    main()
```

### 1.2 Common Text Generation Tasks

```python
"""
02_text_generation_tasks.py - Common text generation use cases
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()


def summarization(text):
    """Summarize long text"""
    print("\n" + "="*60)
    print("SUMMARIZATION")
    print("="*60)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "user",
            "content": f"Summarize this text in 2-3 sentences:\n\n{text}"
        }]
    )

    return response.choices[0].message.content


def translation(text, target_language):
    """Translate text to another language"""
    print("\n" + "="*60)
    print(f"TRANSLATION TO {target_language.upper()}")
    print("="*60)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "user",
            "content": f"Translate this text to {target_language}: '{text}'"
        }]
    )

    return response.choices[0].message.content


def content_generation(topic, content_type):
    """Generate various types of content"""
    print("\n" + "="*60)
    print(f"CONTENT GENERATION: {content_type.upper()}")
    print("="*60)

    prompts = {
        "blog_post": f"Write a 200-word blog post about {topic}",
        "email": f"Write a professional email about {topic}",
        "story": f"Write a short creative story about {topic}",
        "tweet": f"Write an engaging tweet about {topic} (under 280 characters)"
    }

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "user",
            "content": prompts.get(content_type, f"Write about {topic}")
        }]
    )

    return response.choices[0].message.content


def question_answering(context, question):
    """Answer questions based on context"""
    print("\n" + "="*60)
    print("QUESTION ANSWERING")
    print("="*60)

    prompt = f"""Based on the following context, answer the question.

Context: {context}

Question: {question}

Answer:"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0  # More deterministic for Q&A
    )

    return response.choices[0].message.content


def main():
    print("Common Text Generation Tasks")

    # Example 1: Summarization
    long_text = """
    Artificial intelligence (AI) is intelligence demonstrated by machines, as opposed to
    natural intelligence displayed by animals including humans. AI research has been
    defined as the field of study of intelligent agents, which refers to any system that
    perceives its environment and takes actions that maximize its chance of achieving its
    goals. The term "artificial intelligence" had previously been used to describe machines
    that mimic and display "human" cognitive skills that are associated with the human
    mind, such as "learning" and "problem-solving". This definition has since been
    rejected by major AI researchers who now describe AI in terms of rationality and
    acting rationally, which does not limit how intelligence can be articulated.
    """
    summary = summarization(long_text.strip())
    print(f"\nSummary: {summary}")

    # Example 2: Translation
    translation_result = translation("Hello, how are you today?", "Spanish")
    print(f"\nTranslation: {translation_result}")

    # Example 3: Content Generation
    blog_post = content_generation("the benefits of morning exercise", "blog_post")
    print(f"\nBlog Post:\n{blog_post}")

    # Example 4: Question Answering
    context = "Python was created by Guido van Rossum and first released in 1991. Python emphasizes code readability with its use of significant indentation."
    question = "Who created Python?"
    answer = question_answering(context, question)
    print(f"\nAnswer: {answer}")


if __name__ == "__main__":
    main()
```

---

## 2. Code Generation

### 2.1 Generating Code from Natural Language

```python
"""
03_code_generation.py - Generate code from natural language descriptions
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()


def generate_function(description, language="Python"):
    """Generate a function from a description"""
    print("\n" + "="*60)
    print(f"GENERATING {language.upper()} FUNCTION")
    print("="*60)
    print(f"Description: {description}\n")

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": f"You are an expert {language} programmer. Generate clean, well-documented code."
            },
            {
                "role": "user",
                "content": f"Write a {language} function that {description}. Include docstring and comments."
            }
        ],
        temperature=0.2  # Lower temperature for more consistent code
    )

    code = response.choices[0].message.content
    print(code)
    return code


def explain_code(code):
    """Explain what a piece of code does"""
    print("\n" + "="*60)
    print("CODE EXPLANATION")
    print("="*60)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "user",
            "content": f"Explain what this code does line by line:\n\n```python\n{code}\n```"
        }]
    )

    print(response.choices[0].message.content)


def debug_code(buggy_code):
    """Find and fix bugs in code"""
    print("\n" + "="*60)
    print("CODE DEBUGGING")
    print("="*60)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "user",
            "content": f"""Find and fix the bugs in this code. Explain what was wrong and provide the corrected version:

```python
{buggy_code}
```"""
        }]
    )

    print(response.choices[0].message.content)


def refactor_code(code):
    """Improve code quality"""
    print("\n" + "="*60)
    print("CODE REFACTORING")
    print("="*60)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "user",
            "content": f"""Refactor this code to improve readability, efficiency, and follow best practices:

```python
{code}
```"""
        }]
    )

    print(response.choices[0].message.content)


def main():
    print("Code Generation Examples")

    # Example 1: Generate a function
    generate_function("calculates the factorial of a number using recursion")

    # Example 2: Generate a class
    generate_function("creates a BankAccount class with deposit and withdraw methods")

    # Example 3: Explain code
    sample_code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
"""
    explain_code(sample_code.strip())

    # Example 4: Debug code
    buggy = """
def calculate_average(numbers):
    total = 0
    for num in numbers:
        total += num
    return total / len(number)
"""
    debug_code(buggy.strip())


if __name__ == "__main__":
    main()
```

### 2.2 Code Documentation and Testing

```python
"""
04_code_documentation.py - Generate documentation and tests for code
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()


def generate_docstring(function_code):
    """Generate comprehensive docstring for a function"""
    print("\n" + "="*60)
    print("GENERATING DOCSTRING")
    print("="*60)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "user",
            "content": f"""Generate a comprehensive docstring for this function following PEP 257 and Google style guide:

```python
{function_code}
```

Include:
- Brief description
- Args with types
- Returns with type
- Raises (if applicable)
- Example usage"""
        }]
    )

    print(response.choices[0].message.content)


def generate_unit_tests(function_code):
    """Generate unit tests for a function"""
    print("\n" + "="*60)
    print("GENERATING UNIT TESTS")
    print("="*60)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "user",
            "content": f"""Generate comprehensive pytest unit tests for this function:

```python
{function_code}
```

Include:
- Normal cases
- Edge cases
- Error cases
- Multiple test methods"""
        }]
    )

    print(response.choices[0].message.content)


def main():
    sample_function = """
def calculate_bmi(weight_kg, height_m):
    return weight_kg / (height_m ** 2)
"""

    generate_docstring(sample_function.strip())
    generate_unit_tests(sample_function.strip())


if __name__ == "__main__":
    main()
```

---

## 3. Vision and Image Analysis

### 3.1 Analyzing Images with GPT-4 Vision

```python
"""
05_vision_analysis.py - Analyze images with GPT-4 Vision
"""

import os
import base64
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()


def encode_image(image_path):
    """Encode image to base64"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def analyze_image_from_url(image_url, question="What's in this image?"):
    """Analyze an image from a URL"""
    print("\n" + "="*60)
    print("ANALYZING IMAGE FROM URL")
    print("="*60)

    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": question},
                    {
                        "type": "image_url",
                        "image_url": {"url": image_url}
                    }
                ]
            }
        ],
        max_tokens=500
    )

    result = response.choices[0].message.content
    print(f"\nAnalysis: {result}")
    return result


def analyze_local_image(image_path, question="What's in this image?"):
    """Analyze a local image file"""
    print("\n" + "="*60)
    print("ANALYZING LOCAL IMAGE")
    print("="*60)

    # Encode the image
    base64_image = encode_image(image_path)

    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": question},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        max_tokens=500
    )

    result = response.choices[0].message.content
    print(f"\nAnalysis: {result}")
    return result


def multiple_images_analysis(image_urls, question):
    """Analyze multiple images together"""
    print("\n" + "="*60)
    print("ANALYZING MULTIPLE IMAGES")
    print("="*60)

    content = [{"type": "text", "text": question}]

    for url in image_urls:
        content.append({
            "type": "image_url",
            "image_url": {"url": url}
        })

    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[{"role": "user", "content": content}],
        max_tokens=500
    )

    result = response.choices[0].message.content
    print(f"\nAnalysis: {result}")
    return result


def vision_use_cases():
    """Demonstrate various vision use cases"""

    # Example 1: Describe an image
    print("\nUse Case 1: Image Description")
    # analyze_image_from_url("https://example.com/image.jpg", "Describe this image in detail.")

    # Example 2: Object detection
    print("\nUse Case 2: Object Detection")
    # analyze_image_from_url("https://example.com/image.jpg", "List all objects visible in this image.")

    # Example 3: Read text from image (OCR)
    print("\nUse Case 3: Text Extraction (OCR)")
    # analyze_image_from_url("https://example.com/document.jpg", "Extract all text from this image.")

    # Example 4: Image comparison
    print("\nUse Case 4: Image Comparison")
    # multiple_images_analysis(
    #     ["https://example.com/image1.jpg", "https://example.com/image2.jpg"],
    #     "What are the differences between these two images?"
    # )

    print("\nNote: Replace example URLs with actual image URLs to test")


def main():
    print("Vision and Image Analysis")
    vision_use_cases()

    print("\n" + "="*60)
    print("VISION API CAPABILITIES")
    print("="*60)
    print("""
The Vision API can:
- Describe images in detail
- Identify objects, people, and scenes
- Read text from images (OCR)
- Answer questions about images
- Compare multiple images
- Analyze charts, graphs, and diagrams
- Detect emotions and activities
- Identify brands and logos
    """)


if __name__ == "__main__":
    main()
```

### 3.2 Image Generation with DALL-E

```python
"""
06_image_generation.py - Generate images with DALL-E
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()


def generate_image(prompt, size="1024x1024", quality="standard", n=1):
    """Generate an image from a text prompt"""
    print("\n" + "="*60)
    print("GENERATING IMAGE")
    print("="*60)
    print(f"Prompt: {prompt}")
    print(f"Size: {size}, Quality: {quality}\n")

    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size=size,
        quality=quality,
        n=n
    )

    image_url = response.data[0].url
    print(f"Generated image URL: {image_url}")
    print(f"Revised prompt: {response.data[0].revised_prompt}")

    return image_url


def generate_variations(original_image_path, n=2):
    """Generate variations of an existing image"""
    print("\n" + "="*60)
    print("GENERATING IMAGE VARIATIONS")
    print("="*60)

    response = client.images.create_variation(
        image=open(original_image_path, "rb"),
        n=n,
        size="1024x1024"
    )

    for i, image_data in enumerate(response.data):
        print(f"Variation {i+1}: {image_data.url}")


def edit_image(original_image_path, mask_image_path, prompt):
    """Edit an image using a mask"""
    print("\n" + "="*60)
    print("EDITING IMAGE")
    print("="*60)
    print(f"Prompt: {prompt}\n")

    response = client.images.edit(
        image=open(original_image_path, "rb"),
        mask=open(mask_image_path, "rb"),
        prompt=prompt,
        n=1,
        size="1024x1024"
    )

    print(f"Edited image URL: {response.data[0].url}")


def main():
    print("Image Generation with DALL-E")

    # Example prompts
    prompts = [
        "A serene Japanese garden with a red bridge over a koi pond, cherry blossoms, in the style of anime",
        "A futuristic city skyline at sunset with flying cars, cyberpunk style, highly detailed",
        "A cozy coffee shop interior with warm lighting, books on shelves, and a cat sleeping on a chair"
    ]

    print("\nExample 1: Standard quality generation")
    generate_image(prompts[0], size="1024x1024", quality="standard")

    print("\nExample 2: HD quality generation")
    generate_image(prompts[1], size="1024x1024", quality="hd")

    print("\n" + "="*60)
    print("IMAGE GENERATION BEST PRACTICES")
    print("="*60)
    print("""
1. Be specific and detailed in prompts
2. Include style references (e.g., "photorealistic", "oil painting", "anime")
3. Specify lighting, mood, and atmosphere
4. Mention specific elements you want included
5. Use quality="hd" for higher quality (costs more)
6. Available sizes: 1024x1024, 1024x1792, 1792x1024

Example of a good prompt:
"A photorealistic portrait of a elderly fisherman with weathered skin,
wearing a yellow raincoat, on a boat during golden hour, cinematic lighting,
shot with 85mm lens, shallow depth of field"
    """)


if __name__ == "__main__":
    main()
```

---

## 4. Audio and Speech

### 4.1 Speech-to-Text (Whisper)

```python
"""
07_speech_to_text.py - Transcribe audio with Whisper
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()


def transcribe_audio(audio_file_path, language=None):
    """Transcribe audio file to text"""
    print("\n" + "="*60)
    print("TRANSCRIBING AUDIO")
    print("="*60)

    with open(audio_file_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            language=language  # Optional: e.g., "en", "es", "fr"
        )

    print(f"Transcript: {transcript.text}")
    return transcript.text


def transcribe_with_timestamps(audio_file_path):
    """Transcribe audio with word-level timestamps"""
    print("\n" + "="*60)
    print("TRANSCRIBING WITH TIMESTAMPS")
    print("="*60)

    with open(audio_file_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="verbose_json",
            timestamp_granularities=["word"]
        )

    print(f"Full transcript: {transcript.text}\n")

    if hasattr(transcript, 'words'):
        print("Word-level timestamps:")
        for word_info in transcript.words[:10]:  # Show first 10 words
            print(f"  {word_info.word}: {word_info.start}s - {word_info.end}s")


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


def main():
    print("Speech-to-Text with Whisper")

    print("\n" + "="*60)
    print("WHISPER CAPABILITIES")
    print("="*60)
    print("""
Whisper can:
- Transcribe audio in 50+ languages
- Translate audio to English
- Handle various audio formats (mp3, mp4, wav, webm, etc.)
- Process audio up to 25 MB
- Provide word-level timestamps
- Work with noisy audio
- Recognize multiple speakers

Supported formats:
- mp3, mp4, mpeg, mpga, m4a, wav, webm

Example usage:
transcript = transcribe_audio("meeting_recording.mp3", language="en")
translation = translate_audio("spanish_audio.mp3")  # Translates to English
    """)

    # Note: You need actual audio files to test these functions
    # Example:
    # transcribe_audio("path/to/audio.mp3")
    # transcribe_with_timestamps("path/to/audio.mp3")
    # translate_audio("path/to/spanish_audio.mp3")


if __name__ == "__main__":
    main()
```

### 4.2 Text-to-Speech (TTS)

```python
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
```

---

## 5. Structured Outputs

### 5.1 JSON Mode and Structured Outputs

```python
"""
09_structured_outputs.py - Generate structured JSON outputs
"""

import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()


def json_mode_example():
    """Use JSON mode to ensure JSON output"""
    print("\n" + "="*60)
    print("JSON MODE")
    print("="*60)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that outputs in JSON."
            },
            {
                "role": "user",
                "content": "Generate a user profile for John Doe, age 30, occupation software engineer"
            }
        ],
        response_format={"type": "json_object"}
    )

    json_output = json.loads(response.choices[0].message.content)
    print(json.dumps(json_output, indent=2))
    return json_output


def structured_output_with_schema():
    """Generate output conforming to a specific schema"""
    print("\n" + "="*60)
    print("STRUCTURED OUTPUT WITH SCHEMA")
    print("="*60)

    # Define the schema in the prompt
    schema = {
        "name": "string",
        "age": "integer",
        "occupation": "string",
        "skills": ["array", "of", "strings"],
        "contact": {
            "email": "string",
            "phone": "string"
        }
    }

    prompt = f"""Generate a user profile in JSON format following this exact schema:
{json.dumps(schema, indent=2)}

Create a profile for a frontend developer named Sarah Chen."""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You output JSON that strictly follows the provided schema."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        response_format={"type": "json_object"}
    )

    result = json.loads(response.choices[0].message.content)
    print(json.dumps(result, indent=2))
    return result


def extract_structured_data():
    """Extract structured data from unstructured text"""
    print("\n" + "="*60)
    print("EXTRACTING STRUCTURED DATA")
    print("="*60)

    unstructured_text = """
    John Smith is a 35-year-old software engineer living in San Francisco.
    He can be reached at john.smith@email.com or 555-0123.
    He specializes in Python, JavaScript, and cloud architecture.
    He graduated from MIT in 2010 and has been working at TechCorp for 5 years.
    """

    prompt = f"""Extract structured information from this text and return as JSON:

Text: {unstructured_text}

Return JSON with fields: name, age, occupation, location, email, phone, skills (array), education, current_company, years_at_company"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )

    extracted_data = json.loads(response.choices[0].message.content)
    print(json.dumps(extracted_data, indent=2))
    return extracted_data


def generate_multiple_records():
    """Generate multiple structured records"""
    print("\n" + "="*60)
    print("GENERATING MULTIPLE RECORDS")
    print("="*60)

    prompt = """Generate 3 fictional product records in JSON format.
Each product should have: id, name, price, category, in_stock (boolean), description.
Return as a JSON array."""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )

    products = json.loads(response.choices[0].message.content)
    print(json.dumps(products, indent=2))
    return products


def main():
    print("Structured Outputs and JSON Mode")

    json_mode_example()
    structured_output_with_schema()
    extract_structured_data()
    generate_multiple_records()

    print("\n" + "="*60)
    print("STRUCTURED OUTPUT USE CASES")
    print("="*60)
    print("""
Common Use Cases:
1. API responses - Return data in consistent format
2. Database records - Generate structured data for storage
3. Form data - Extract information from text into forms
4. Configuration files - Generate config in JSON format
5. Data transformation - Convert unstructured to structured
6. Validation - Ensure output matches expected schema

Best Practices:
- Always specify response_format={"type": "json_object"}
- Define clear schemas in prompts
- Validate the output JSON
- Handle parsing errors gracefully
- Use Pydantic or similar for schema validation
    """)


if __name__ == "__main__":
    main()
```

---

## 6. Function Calling

### 6.1 Basic Function Calling

```python
"""
10_function_calling.py - Implement function calling for tool use
"""

import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()


# Define tools/functions the model can call
def get_weather(location, unit="celsius"):
    """Simulated weather API"""
    # In reality, this would call a real weather API
    weather_data = {
        "San Francisco": {"temp": 18, "condition": "Partly cloudy"},
        "New York": {"temp": 22, "condition": "Sunny"},
        "London": {"temp": 15, "condition": "Rainy"},
        "Tokyo": {"temp": 25, "condition": "Clear"}
    }

    data = weather_data.get(location, {"temp": 20, "condition": "Unknown"})
    return json.dumps(data)


def calculate(operation, num1, num2):
    """Perform mathematical operations"""
    operations = {
        "add": num1 + num2,
        "subtract": num1 - num2,
        "multiply": num1 * num2,
        "divide": num1 / num2 if num2 != 0 else "Error: Division by zero"
    }
    result = operations.get(operation, "Unknown operation")
    return json.dumps({"result": result})


# Define function schemas for the model
functions = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city name, e.g., San Francisco"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "Temperature unit"
                    }
                },
                "required": ["location"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Perform mathematical calculations",
            "parameters": {
                "type": "object",
                "properties": {
                    "operation": {
                        "type": "string",
                        "enum": ["add", "subtract", "multiply", "divide"],
                        "description": "The mathematical operation to perform"
                    },
                    "num1": {
                        "type": "number",
                        "description": "First number"
                    },
                    "num2": {
                        "type": "number",
                        "description": "Second number"
                    }
                },
                "required": ["operation", "num1", "num2"]
            }
        }
    }
]


def function_calling_example(user_query):
    """Demonstrate function calling"""
    print("\n" + "="*60)
    print("FUNCTION CALLING EXAMPLE")
    print("="*60)
    print(f"User Query: {user_query}\n")

    # Step 1: Send the query with available functions
    messages = [{"role": "user", "content": user_query}]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        tools=functions,
        tool_choice="auto"
    )

    response_message = response.choices[0].message
    messages.append(response_message)

    # Step 2: Check if the model wants to call a function
    tool_calls = response_message.tool_calls

    if tool_calls:
        # Step 3: Execute the function calls
        available_functions = {
            "get_weather": get_weather,
            "calculate": calculate
        }

        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)

            print(f"Calling function: {function_name}")
            print(f"Arguments: {function_args}")

            # Call the function
            function_to_call = available_functions[function_name]
            function_response = function_to_call(**function_args)

            print(f"Function response: {function_response}\n")

            # Step 4: Add function response to messages
            messages.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": function_response
            })

        # Step 5: Get final response from model
        second_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        final_answer = second_response.choices[0].message.content
        print(f"Final Answer: {final_answer}")
        return final_answer

    else:
        # No function call needed
        return response_message.content


def main():
    print("Function Calling for Tool Use")

    # Example 1: Weather query
    function_calling_example("What's the weather like in San Francisco?")

    # Example 2: Math calculation
    function_calling_example("What is 234 multiplied by 567?")

    # Example 3: Multiple operations
    function_calling_example("What's the weather in Tokyo and what is 100 divided by 4?")

    print("\n" + "="*60)
    print("FUNCTION CALLING CONCEPTS")
    print("="*60)
    print("""
Function calling allows models to:
- Use external tools and APIs
- Access real-time data
- Perform calculations
- Query databases
- Interact with services

Flow:
1. Define available functions with schemas
2. Send user query with function definitions
3. Model decides which function(s) to call
4. Execute the function(s)
5. Send results back to model
6. Model formulates final response

Key Parameters:
- tools: Array of function definitions
- tool_choice: "auto", "none", or specific function
- parallel_tool_calls: Allow multiple functions at once

Use Cases:
- Database queries
- API integrations
- Calculations and data processing
- Booking systems
- IoT device control
- Custom business logic
    """)


if __name__ == "__main__":
    main()
```

---

## 7. Multi-Modal Applications

### 7.1 Combining Multiple Modalities

```python
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
            model="gpt-4-vision-preview",
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
```

---

## Exercises

### Exercise 1: Advanced Chatbot
Build a chatbot that:
- Uses few-shot prompting for specific tasks
- Maintains context across conversations
- Can switch between different personalities
- Implements proper error handling

### Exercise 2: Code Assistant
Create a code assistant that:
- Generates code from descriptions
- Explains existing code
- Suggests improvements
- Generates unit tests
- Finds and fixes bugs

### Exercise 3: Image Analyzer
Build an application that:
- Accepts image uploads
- Analyzes image content
- Extracts text (OCR)
- Generates descriptions
- Answers questions about the image

### Exercise 4: Audio Transcription Service
Create a service that:
- Transcribes audio files
- Provides word-level timestamps
- Summarizes transcripts
- Extracts key points
- Generates meeting notes

### Exercise 5: Data Extraction Tool
Build a tool that:
- Extracts structured data from unstructured text
- Validates against schemas
- Handles multiple record types
- Exports to JSON/CSV

### Exercise 6: Function-Calling Agent
Create an agent that can:
- Access multiple external tools
- Make decisions about which tools to use
- Handle multi-step tasks
- Provide progress updates

---

## Summary

### Key Takeaways

✅ **What We Learned**:
- Advanced text generation techniques (zero-shot, few-shot, chain-of-thought)
- Code generation, explanation, debugging, and documentation
- Vision capabilities for image analysis
- Image generation with DALL-E
- Speech-to-text with Whisper
- Text-to-speech for audio generation
- Structured JSON outputs with schemas
- Function calling for tool use
- Building multi-modal applications

✅ **Skills Acquired**:
- Crafting effective prompts for different tasks
- Generating and working with code
- Processing images and vision data
- Handling audio transcription and generation
- Creating structured, machine-readable outputs
- Implementing function calling patterns
- Combining multiple modalities

### Best Practices Recap

1. ✅ Use appropriate prompting techniques for your task
2. ✅ Lower temperature (0-0.3) for consistent, focused outputs
3. ✅ Higher temperature (0.7-1.5) for creative tasks
4. ✅ Use JSON mode for structured outputs
5. ✅ Define clear function schemas for tool use
6. ✅ Handle errors gracefully across all modalities
7. ✅ Test with different models to find the best fit

### Next Steps

In **Module 4: API Reference and Authentication**, you'll learn:
- Deep dive into API authentication
- Rate limiting strategies
- Request debugging and monitoring
- API versioning and compatibility
- Multi-organization access

---

[⬅️ Previous: Module 2](../module-02-getting-started/README.md) | [Home](../README.md) | [Next: Module 4 ➡️](../module-04-api-reference/README.md)
