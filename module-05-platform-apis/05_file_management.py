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
