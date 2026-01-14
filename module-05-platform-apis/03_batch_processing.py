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
