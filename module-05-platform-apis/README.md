# Module 5: Platform APIs

## 📋 Module Overview

**Duration**: 3-4 hours
**Level**: Intermediate to Advanced
**Prerequisites**: Modules 1-4 completed

Explore the full range of OpenAI platform capabilities including embeddings, fine-tuning, batch processing, and content moderation.

---

## 🎯 Learning Objectives

- ✅ Work with embeddings for semantic search
- ✅ Fine-tune models for custom use cases
- ✅ Implement batch processing for efficiency
- ✅ Use content moderation APIs
- ✅ Manage files and uploads
- ✅ Work with webhooks for event-driven architecture

---

## 📖 Table of Contents

1. [Embeddings](#1-embeddings)
2. [Fine-Tuning](#2-fine-tuning)
3. [Batch Processing](#3-batch-processing)
4. [Content Moderation](#4-content-moderation)
5. [File Management](#5-file-management)
6. [Webhooks](#6-webhooks)

---

## 1. Embeddings

### 1.1 Creating and Using Embeddings

```python
"""
01_embeddings.py - Work with text embeddings
"""

import os
import numpy as np
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()


def get_embedding(text, model="text-embedding-3-small"):
    """Get embedding for text"""
    text = text.replace("\n", " ")
    response = client.embeddings.create(input=[text], model=model)
    return response.data[0].embedding


def cosine_similarity(vec1, vec2):
    """Calculate cosine similarity between two vectors"""
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))


def semantic_search_example():
    """Demonstrate semantic search with embeddings"""
    print("\n" + "="*60)
    print("SEMANTIC SEARCH WITH EMBEDDINGS")
    print("="*60)

    # Sample documents
    documents = [
        "Python is a high-level programming language",
        "Machine learning is a subset of artificial intelligence",
        "The cat sat on the mat",
        "Deep learning uses neural networks with multiple layers",
        "JavaScript is used for web development"
    ]

    # Create embeddings for all documents
    doc_embeddings = [get_embedding(doc) for doc in documents]

    # Search query
    query = "artificial intelligence and neural networks"
    query_embedding = get_embedding(query)

    # Calculate similarities
    similarities = [
        cosine_similarity(query_embedding, doc_emb)
        for doc_emb in doc_embeddings
    ]

    # Get most similar documents
    ranked_docs = sorted(
        zip(documents, similarities),
        key=lambda x: x[1],
        reverse=True
    )

    print(f"\nQuery: {query}\n")
    print("Most relevant documents:")
    for doc, score in ranked_docs[:3]:
        print(f"  Score: {score:.4f} - {doc}")


def text_clustering_example():
    """Cluster similar texts using embeddings"""
    print("\n" + "="*60)
    print("TEXT CLUSTERING")
    print("="*60)

    texts = [
        "Machine learning algorithms",
        "Deep neural networks",
        "Pizza and pasta recipes",
        "Italian cuisine cooking",
        "Python programming tutorial",
        "JavaScript web development"
    ]

    # Get embeddings
    embeddings = [get_embedding(text) for text in texts]

    # Simple clustering: find pairs with high similarity
    print("\nSimilar text pairs:")
    for i in range(len(texts)):
        for j in range(i + 1, len(texts)):
            similarity = cosine_similarity(embeddings[i], embeddings[j])
            if similarity > 0.8:  # High similarity threshold
                print(f"  {texts[i]} <-> {texts[j]}: {similarity:.4f}")


# Embedding Models
embedding_guide = """
EMBEDDING MODELS:

Available Models:
1. text-embedding-3-small
   - Dimensions: 1536
   - Performance: Fast, efficient
   - Cost: Lowest
   - Use: General purpose

2. text-embedding-3-large
   - Dimensions: 3072
   - Performance: Highest quality
   - Cost: Higher
   - Use: When accuracy matters

3. text-embedding-ada-002 (Legacy)
   - Dimensions: 1536
   - Still supported
   - Use new models for better performance

Common Use Cases:
- Semantic search
- Recommendation systems
- Clustering and classification
- Anomaly detection
- Similarity comparison

Best Practices:
- Normalize embeddings for cosine similarity
- Cache embeddings (they're deterministic)
- Use appropriate model for your use case
- Batch requests for efficiency
"""

print(embedding_guide)


if __name__ == "__main__":
    semantic_search_example()
    text_clustering_example()
```

---

## 2. Fine-Tuning

### 2.1 Fine-Tuning Custom Models

```python
"""
02_fine_tuning.py - Fine-tune models for specific use cases
"""

import os
import json
import time
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()


def create_training_file():
    """Create JSONL training file for fine-tuning"""
    training_data = [
        {
            "messages": [
                {"role": "system", "content": "You are a helpful customer support assistant."},
                {"role": "user", "content": "How do I reset my password?"},
                {"role": "assistant", "content": "To reset your password, go to Settings > Security > Reset Password. You'll receive an email with instructions."}
            ]
        },
        {
            "messages": [
                {"role": "system", "content": "You are a helpful customer support assistant."},
                {"role": "user", "content": "Where can I track my order?"},
                {"role": "assistant", "content": "You can track your order by visiting My Orders in your account dashboard or using the tracking link in your confirmation email."}
            ]
        },
        # Add more training examples...
    ]

    # Save as JSONL
    with open("training_data.jsonl", "w") as f:
        for item in training_data:
            f.write(json.dumps(item) + "\n")

    print("✅ Training file created: training_data.jsonl")
    return "training_data.jsonl"


def upload_training_file(file_path):
    """Upload training file to OpenAI"""
    print(f"\n📤 Uploading training file: {file_path}")

    with open(file_path, "rb") as file:
        response = client.files.create(
            file=file,
            purpose="fine-tune"
        )

    print(f"✅ File uploaded: {response.id}")
    return response.id


def create_fine_tune_job(training_file_id, model="gpt-3.5-turbo"):
    """Create a fine-tuning job"""
    print(f"\n🚀 Starting fine-tuning job...")

    response = client.fine_tuning.jobs.create(
        training_file=training_file_id,
        model=model,
        hyperparameters={
            "n_epochs": 3  # Number of training epochs
        }
    )

    print(f"✅ Fine-tuning job created: {response.id}")
    print(f"   Status: {response.status}")

    return response.id


def monitor_fine_tune_job(job_id):
    """Monitor fine-tuning job progress"""
    print(f"\n👀 Monitoring job: {job_id}")

    while True:
        job = client.fine_tuning.jobs.retrieve(job_id)
        status = job.status

        print(f"Status: {status}")

        if status in ["succeeded", "failed", "cancelled"]:
            break

        time.sleep(60)  # Check every minute

    if status == "succeeded":
        print(f"✅ Fine-tuning completed!")
        print(f"   Fine-tuned model: {job.fine_tuned_model}")
        return job.fine_tuned_model
    else:
        print(f"❌ Fine-tuning {status}")
        return None


def use_fine_tuned_model(model_name, prompt):
    """Use a fine-tuned model"""
    print(f"\n🤖 Using fine-tuned model: {model_name}")

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


fine_tuning_guide = """
FINE-TUNING GUIDE:

When to Fine-Tune:
✅ Domain-specific terminology
✅ Consistent output format
✅ Specific tone/style
✅ Custom behavior patterns

When NOT to Fine-Tune:
❌ Limited training data (need 50+ examples)
❌ Can be solved with prompting
❌ Frequently changing requirements

Training Data Requirements:
- Minimum: 10 examples (50+ recommended)
- Format: JSONL with messages array
- Quality over quantity
- Diverse examples
- Consistent formatting

Fine-Tuning Process:
1. Prepare training data (JSONL format)
2. Upload training file
3. Create fine-tuning job
4. Monitor progress
5. Use fine-tuned model

Cost Considerations:
- Training cost: Per token in training data
- Usage cost: Same as base model
- Storage: Model stored indefinitely

Best Practices:
- Start with good prompts first
- Use validation set to check overfitting
- Iterate on training data
- Monitor performance metrics
- Version your fine-tuned models
"""

print(fine_tuning_guide)
```

---

## 3. Batch Processing

### 3.1 Efficient Batch Operations

```python
"""
03_batch_processing.py - Process multiple requests efficiently
"""

import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()


def create_batch_input_file(requests):
    """Create batch input file"""
    with open("batch_input.jsonl", "w") as f:
        for i, request in enumerate(requests):
            batch_request = {
                "custom_id": f"request-{i}",
                "method": "POST",
                "url": "/v1/chat/completions",
                "body": {
                    "model": "gpt-3.5-turbo",
                    "messages": [{"role": "user", "content": request}],
                    "max_tokens": 100
                }
            }
            f.write(json.dumps(batch_request) + "\n")

    return "batch_input.jsonl"


def submit_batch_job(input_file_path):
    """Submit batch processing job"""
    print(f"\n📤 Submitting batch job...")

    # Upload input file
    with open(input_file_path, "rb") as file:
        batch_input_file = client.files.create(
            file=file,
            purpose="batch"
        )

    # Create batch job
    batch_job = client.batches.create(
        input_file_id=batch_input_file.id,
        endpoint="/v1/chat/completions",
        completion_window="24h"
    )

    print(f"✅ Batch job created: {batch_job.id}")
    print(f"   Status: {batch_job.status}")

    return batch_job.id


def check_batch_status(batch_id):
    """Check batch job status"""
    batch = client.batches.retrieve(batch_id)

    print(f"\nBatch Status: {batch.status}")
    print(f"Total requests: {batch.request_counts.total}")
    print(f"Completed: {batch.request_counts.completed}")
    print(f"Failed: {batch.request_counts.failed}")

    return batch


def retrieve_batch_results(batch_id):
    """Retrieve batch results"""
    batch = client.batches.retrieve(batch_id)

    if batch.status != "completed":
        print(f"Batch not completed yet. Status: {batch.status}")
        return None

    # Download results
    result_file_id = batch.output_file_id
    results = client.files.content(result_file_id)

    # Parse results
    results_data = []
    for line in results.text.strip().split('\n'):
        results_data.append(json.loads(line))

    return results_data


batch_guide = """
BATCH PROCESSING GUIDE:

Benefits:
- 50% cost savings compared to real-time
- Process large volumes efficiently
- No rate limits for batch
- Results within 24 hours

Use Cases:
- Bulk content generation
- Large-scale data processing
- Evaluation and testing
- Historical data analysis

Limitations:
- Not real-time (up to 24 hours)
- Cannot cancel individual requests
- Results expire after 24 hours

Best Practices:
- Use for non-urgent workloads
- Group similar requests together
- Include custom_id for tracking
- Monitor completion status
- Download results promptly

Batch vs Real-Time:
- Batch: 50% cheaper, up to 24h delay
- Real-Time: Full price, immediate results
"""

print(batch_guide)
```

---

## 4. Content Moderation

### 4.1 Moderating Content for Safety

```python
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
```

---

## 5. File Management

### 5.1 Managing Files and Uploads

```python
"""
05_file_management.py - Manage files in OpenAI platform
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()


def upload_file(file_path, purpose="assistants"):
    """Upload a file to OpenAI"""
    print(f"\n📤 Uploading file: {file_path}")

    with open(file_path, "rb") as file:
        response = client.files.create(
            file=file,
            purpose=purpose  # "assistants", "fine-tune", "batch"
        )

    print(f"✅ File uploaded: {response.id}")
    print(f"   Filename: {response.filename}")
    print(f"   Size: {response.bytes} bytes")

    return response.id


def list_files():
    """List all uploaded files"""
    print("\n📋 Listing files...")

    files = client.files.list()

    for file in files.data:
        print(f"\nFile ID: {file.id}")
        print(f"  Filename: {file.filename}")
        print(f"  Purpose: {file.purpose}")
        print(f"  Size: {file.bytes} bytes")
        print(f"  Created: {file.created_at}")


def retrieve_file_info(file_id):
    """Get file information"""
    print(f"\nℹ️  Retrieving file info: {file_id}")

    file = client.files.retrieve(file_id)

    print(f"Filename: {file.filename}")
    print(f"Purpose: {file.purpose}")
    print(f"Size: {file.bytes} bytes")

    return file


def download_file(file_id, output_path):
    """Download a file"""
    print(f"\n⬇️  Downloading file: {file_id}")

    content = client.files.content(file_id)

    with open(output_path, "wb") as f:
        f.write(content.content)

    print(f"✅ File downloaded to: {output_path}")


def delete_file(file_id):
    """Delete a file"""
    print(f"\n🗑️  Deleting file: {file_id}")

    client.files.delete(file_id)

    print(f"✅ File deleted: {file_id}")


file_management_guide = """
FILE MANAGEMENT GUIDE:

Purposes:
- assistants: For Assistants API
- fine-tune: For fine-tuning
- batch: For batch processing

Supported Formats:
- Documents: .pdf, .doc, .docx, .txt
- Data: .json, .jsonl, .csv
- Images: .png, .jpg, .gif
- Audio: .mp3, .mp4, .wav

Size Limits:
- Max file size: 512 MB
- Batch files: Larger limits

Best Practices:
- Delete unused files to manage storage
- Use descriptive filenames
- Set appropriate purpose
- Track file IDs
- Monitor storage usage

Common Operations:
1. Upload: client.files.create()
2. List: client.files.list()
3. Retrieve: client.files.retrieve()
4. Download: client.files.content()
5. Delete: client.files.delete()
"""

print(file_management_guide)
```

---

## 6. Webhooks

### 6.1 Event-Driven Architecture

```python
"""
06_webhooks.py - Implement webhooks for event-driven architecture
"""

webhook_guide = """
WEBHOOKS GUIDE:

What are Webhooks?
- HTTP callbacks for events
- Real-time notifications
- Event-driven architecture

Supported Events:
- fine_tuning.job.completed
- fine_tuning.job.failed
- batch.completed
- batch.failed

Setup:
1. Create webhook endpoint (your server)
2. Register endpoint with OpenAI
3. Verify webhook signatures
4. Handle events

Example Webhook Handler (Flask):

from flask import Flask, request
import hmac
import hashlib

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    # Get signature from header
    signature = request.headers.get('X-OpenAI-Signature')

    # Verify signature
    secret = os.getenv('WEBHOOK_SECRET')
    computed_sig = hmac.new(
        secret.encode(),
        request.data,
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(signature, computed_sig):
        return 'Invalid signature', 401

    # Process event
    event = request.json
    event_type = event['type']

    if event_type == 'fine_tuning.job.completed':
        handle_fine_tune_complete(event)
    elif event_type == 'batch.completed':
        handle_batch_complete(event)

    return 'OK', 200

Security:
- Always verify signatures
- Use HTTPS only
- Implement idempotency
- Handle duplicates
- Log all events

Best Practices:
- Process events asynchronously
- Implement retry logic
- Return 200 quickly
- Don't do heavy processing in handler
- Use queues for processing
"""

print(webhook_guide)
```

---

## Summary

✅ **Key Learnings**:
- Embeddings for semantic search and similarity
- Fine-tuning custom models
- Batch processing for efficiency
- Content moderation for safety
- File management operations
- Webhooks for event-driven architecture

✅ **Skills Acquired**:
- Creating and using embeddings
- Fine-tuning workflow
- Batch job management
- Implementing content moderation
- File upload/download operations
- Webhook integration

---

[⬅️ Previous: Module 4](../module-04-api-reference/README.md) | [Home](../README.md) | [Next: Module 6 ➡️](../module-06-specialized-features/README.md)
