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
