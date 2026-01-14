"""
02_fine_tuning.py - Create and manage fine-tuning jobs
"""

import os
import json
import time
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()


def create_training_file(filename="training_data.jsonl"):
    """Create a sample training file"""
    data = [
        {
            "messages": [
                {"role": "system", "content": "You are a sarcastic chatbot."},
                {"role": "user", "content": "What is the capital of France?"},
                {"role": "assistant", "content": "Paris, obviously. Did you sleep through geography?"}
            ]
        },
        {
            "messages": [
                {"role": "system", "content": "You are a sarcastic chatbot."},
                {"role": "user", "content": "Who wrote Romeo and Juliet?"},
                {"role": "assistant", "content": "Shakespeare. Heard of him? Or do you live under a rock?"}
            ]
        },
        {
            "messages": [
                {"role": "system", "content": "You are a sarcastic chatbot."},
                {"role": "user", "content": "What is 2+2?"},
                {"role": "assistant", "content": "It's 4. I can't believe I have to answer that."}
            ]
        }
    ]

    with open(filename, "w") as f:
        for entry in data:
            f.write(json.dumps(entry) + "\n")

    print(f"Created training file: {filename}")
    return filename


def upload_file(filename):
    """Upload file for fine-tuning"""
    print(f"Uploading {filename}...")
    file = client.files.create(
        file=open(filename, "rb"),
        purpose="fine-tune"
    )
    print(f"File uploaded. ID: {file.id}")
    return file.id


def create_fine_tune_job(file_id, model="gpt-3.5-turbo"):
    """Start a fine-tuning job"""
    print(f"Starting fine-tuning job with file {file_id}...")
    job = client.fine_tuning.jobs.create(
        training_file=file_id,
        model=model
    )
    print(f"Job created. ID: {job.id}")
    return job.id


def monitor_job(job_id):
    """Monitor fine-tuning job status"""
    print(f"Monitoring job {job_id}...")

    while True:
        job = client.fine_tuning.jobs.retrieve(job_id)
        print(f"Status: {job.status}")

        if job.status in ["succeeded", "failed", "cancelled"]:
            break

        time.sleep(10)

    if job.status == "succeeded":
        print(f"Fine-tuning completed! New model: {job.fine_tuned_model}")
        return job.fine_tuned_model
    else:
        print("Fine-tuning failed.")
        return None


def use_fine_tuned_model(model_id, prompt):
    """Test the fine-tuned model"""
    print(f"\nTesting model {model_id}...")
    response = client.chat.completions.create(
        model=model_id,
        messages=[
            {"role": "system", "content": "You are a sarcastic chatbot."},
            {"role": "user", "content": prompt}
        ]
    )
    print(f"Response: {response.choices[0].message.content}")


def main():
    print("Fine-Tuning Demo")

    # NOTE: Fine-tuning costs money and takes time.
    # Uncomment steps to run actual fine-tuning.

    # 1. Create data
    # filename = create_training_file()

    # 2. Upload file
    # file_id = upload_file(filename)

    # 3. Create job
    # job_id = create_fine_tune_job(file_id)

    # 4. Monitor
    # model_id = monitor_job(job_id)

    # 5. Use model
    # if model_id:
    #     use_fine_tuned_model(model_id, "What color is the sky?")

    print("\nSteps commented out to prevent accidental charges.")
    print("Check the code to enable fine-tuning steps.")


if __name__ == "__main__":
    main()
