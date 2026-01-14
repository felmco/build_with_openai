# OpenAI API Quick Reference

## 🚀 Quick Start

```python
from openai import OpenAI
client = OpenAI()  # Reads OPENAI_API_KEY from environment

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.choices[0].message.content)
```

---

## 📚 Common Patterns

### Basic Chat
```python
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ]
)
```

### With Parameters
```python
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Tell me a joke"}],
    temperature=0.7,      # 0-2, higher = more creative
    max_tokens=100,       # Limit response length
    top_p=1,             # Nucleus sampling
    frequency_penalty=0,  # -2 to 2, penalize repetition
    presence_penalty=0    # -2 to 2, encourage new topics
)
```

### Streaming Response
```python
stream = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Count to 10"}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

### Error Handling
```python
from openai import APIError, RateLimitError, APIConnectionError

try:
    response = client.chat.completions.create(...)
except RateLimitError:
    # Handle rate limit
    time.sleep(60)
except APIConnectionError:
    # Handle connection error
    pass
except APIError as e:
    # Handle other errors
    print(f"Error: {e}")
```

---

## 🎨 Images (DALL-E)

### Generate Image
```python
response = client.images.generate(
    model="dall-e-3",
    prompt="A serene mountain landscape at sunset",
    size="1024x1024",  # "1024x1024", "1792x1024", "1024x1792"
    quality="standard", # "standard" or "hd"
    n=1
)
image_url = response.data[0].url
```

---

## 🎙️ Audio

### Speech-to-Text (Whisper)
```python
with open("audio.mp3", "rb") as audio_file:
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        language="en"  # Optional
    )
print(transcript.text)
```

### Text-to-Speech
```python
response = client.audio.speech.create(
    model="tts-1",  # or "tts-1-hd"
    voice="alloy",  # alloy, echo, fable, onyx, nova, shimmer
    input="Hello, how are you today?"
)
response.stream_to_file("output.mp3")
```

---

## 👁️ Vision (GPT-4 Vision)

### Analyze Image from URL
```python
response = client.chat.completions.create(
    model="gpt-4-vision-preview",
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "What's in this image?"},
            {"type": "image_url", "image_url": {"url": "https://..."}}
        ]
    }],
    max_tokens=300
)
```

### Analyze Local Image
```python
import base64

def encode_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode('utf-8')

base64_image = encode_image("image.jpg")

response = client.chat.completions.create(
    model="gpt-4-vision-preview",
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "Describe this image"},
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }
            }
        ]
    }]
)
```

---

## 🔢 Embeddings

### Create Embeddings
```python
response = client.embeddings.create(
    model="text-embedding-3-small",
    input="Your text here"
)
embedding = response.data[0].embedding  # List of floats
```

### Cosine Similarity
```python
import numpy as np

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

similarity = cosine_similarity(embedding1, embedding2)
```

---

## 🛠️ Function Calling

### Define Functions
```python
functions = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get weather for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City name"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"]
                    }
                },
                "required": ["location"]
            }
        }
    }
]
```

### Use Functions
```python
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "What's the weather in Paris?"}],
    tools=functions,
    tool_choice="auto"
)

# Check if function was called
if response.choices[0].message.tool_calls:
    tool_call = response.choices[0].message.tool_calls[0]
    function_name = tool_call.function.name
    arguments = json.loads(tool_call.function.arguments)

    # Execute function and send back
    result = get_weather(**arguments)

    messages.append(response.choices[0].message)
    messages.append({
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": result
    })

    # Get final response
    final_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
```

---

## 📦 Structured Outputs (JSON Mode)

```python
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "system",
            "content": "You output JSON only."
        },
        {
            "role": "user",
            "content": "Generate a user profile for John, age 30"
        }
    ],
    response_format={"type": "json_object"}
)

data = json.loads(response.choices[0].message.content)
```

---

## 🔒 Content Moderation

```python
response = client.moderations.create(input="Text to moderate")
result = response.results[0]

if result.flagged:
    print("Content flagged!")
    print(result.categories)  # hate, violence, sexual, etc.
    print(result.category_scores)
```

---

## 📁 File Operations

### Upload File
```python
with open("data.jsonl", "rb") as f:
    file = client.files.create(
        file=f,
        purpose="fine-tune"  # or "assistants", "batch"
    )
print(file.id)
```

### List Files
```python
files = client.files.list()
for file in files.data:
    print(f"{file.id}: {file.filename}")
```

### Delete File
```python
client.files.delete(file_id)
```

---

## 🎯 Fine-Tuning

### Create Fine-Tuning Job
```python
job = client.fine_tuning.jobs.create(
    training_file="file-abc123",
    model="gpt-3.5-turbo"
)
```

### Check Status
```python
job = client.fine_tuning.jobs.retrieve(job_id)
print(job.status)  # "queued", "running", "succeeded", "failed"
```

### Use Fine-Tuned Model
```python
response = client.chat.completions.create(
    model="ft:gpt-3.5-turbo:org:model:id",
    messages=[{"role": "user", "content": "Hello"}]
)
```

---

## 📊 Batch Processing

### Create Batch
```python
batch = client.batches.create(
    input_file_id="file-abc123",
    endpoint="/v1/chat/completions",
    completion_window="24h"
)
```

### Check Batch Status
```python
batch = client.batches.retrieve(batch_id)
print(f"Status: {batch.status}")
print(f"Completed: {batch.request_counts.completed}")
```

---

## 🤖 Assistants API

### Create Assistant
```python
assistant = client.beta.assistants.create(
    name="Math Tutor",
    instructions="You are a helpful math tutor",
    model="gpt-4-turbo",
    tools=[{"type": "code_interpreter"}]
)
```

### Create Thread
```python
thread = client.beta.threads.create()
```

### Add Message
```python
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="Solve: 3x + 11 = 14"
)
```

### Run Assistant
```python
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id
)

# Wait for completion
while run.status != "completed":
    run = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    )
    time.sleep(1)

# Get messages
messages = client.beta.threads.messages.list(thread_id=thread.id)
```

---

## 📈 Best Practices Checklist

### Security
- [ ] Store API key in environment variables
- [ ] Add `.env` to `.gitignore`
- [ ] Rotate keys regularly
- [ ] Use different keys for dev/prod
- [ ] Never commit keys to version control

### Performance
- [ ] Set `max_tokens` to control costs
- [ ] Use appropriate model (GPT-3.5 vs GPT-4)
- [ ] Implement caching for common queries
- [ ] Use batch processing for large jobs
- [ ] Stream responses for better UX

### Reliability
- [ ] Implement exponential backoff for retries
- [ ] Handle all exception types
- [ ] Monitor rate limits
- [ ] Log all API calls
- [ ] Set reasonable timeouts

### Cost Optimization
- [ ] Use GPT-3.5-turbo when possible
- [ ] Trim conversation history
- [ ] Cache responses
- [ ] Use batch API (50% savings)
- [ ] Monitor token usage

---

## 📊 Model Comparison

| Model | Speed | Cost | Best For |
|-------|-------|------|----------|
| gpt-3.5-turbo | ⚡⚡⚡ | $ | General chat, simple tasks |
| gpt-4 | ⚡ | $$$ | Complex reasoning, accuracy |
| gpt-4-turbo | ⚡⚡ | $$ | Balanced performance |
| gpt-4-vision-preview | ⚡ | $$$ | Image analysis |
| dall-e-3 | ⚡ | $$ | Image generation |
| whisper-1 | ⚡⚡ | $ | Speech-to-text |
| tts-1 | ⚡⚡ | $ | Text-to-speech |
| text-embedding-3-small | ⚡⚡⚡ | $ | Embeddings |

---

## 🔗 Quick Links

- **Documentation**: https://platform.openai.com/docs
- **API Reference**: https://platform.openai.com/docs/api-reference
- **Pricing**: https://openai.com/pricing
- **Status**: https://status.openai.com
- **Cookbook**: https://github.com/openai/openai-cookbook
- **Forum**: https://community.openai.com

---

## 💡 Common Gotchas

1. **Token Limits**: Each model has max context length
2. **Rate Limits**: Implement exponential backoff
3. **JSON Mode**: Must mention "JSON" in prompt
4. **Function Calling**: Only works with specific models
5. **Image Size**: DALL-E 3 only supports specific sizes
6. **Audio Length**: Whisper max 25MB files
7. **Vision**: Not all GPT-4 variants support images

---

**Quick Reference Version**: 1.0.0
**Last Updated**: January 2026
