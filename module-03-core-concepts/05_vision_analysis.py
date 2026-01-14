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
        model="gpt-4o",
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
        model="gpt-4o",
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
        model="gpt-4o",
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
