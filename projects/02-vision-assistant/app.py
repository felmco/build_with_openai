"""
Project 2: Vision Sales Assistant
---------------------------------
This script demonstrates multimodal capabilities using GPT-4o.
It takes an image (URL or local path) and generates structured product data.
"""

import os
import base64
import requests
from openai import OpenAI
from pydantic import BaseModel, Field
from typing import List

# Initialize client
client = OpenAI()

# --- Data Structures ---

class ProductAnalysis(BaseModel):
    """Structured output for product analysis"""
    title: str = Field(description="SEO optimized product title (50-60 chars)")
    description: str = Field(description="Engaging marketing description (2-3 sentences)")
    features: List[str] = Field(description="List of 3 key visual features")
    tags: List[str] = Field(description="5-8 relevant search keywords")
    estimated_category: str = Field(description="e.g. Electronics, Fashion, Home")
    visual_condition: str = Field(description="Assessment of item condition based on image")

# --- Helper Functions ---

def encode_image(image_path):
    """Encodes a local image to base64"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def analyze_image(image_input: str, is_url: bool = True) -> ProductAnalysis:
    """
    Analyzes an image using GPT-4o with structured output.
    """
    print(f"\n👀 Analyzing image...")

    # Prepare input based on URL or local file
    if is_url:
        image_content = {"url": image_input}
    else:
        # For local files, we need data URI format
        base64_image = encode_image(image_input)
        image_content = {"url": f"data:image/jpeg;base64,{base64_image}"}

    try:
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[
                {
                    "role": "system", 
                    "content": "You are an expert e-commerce copywriter. Analyze the product image and generate listing details."
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Analyze this product image and provide listing details."},
                        {"type": "image_url", "image_url": image_content}
                    ]
                }
            ],
            response_format=ProductAnalysis
        )
        return completion.choices[0].message.parsed
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return None

# --- Main Application ---

def main():
    print("🛍️ VISION SALES ASSISTANT")
    print("="*60)
    
    choice = input("Enter (1) for Image URL or (2) for Local File Path: ")
    
    image_input = ""
    is_url = True
    
    if choice == "1":
        image_input = input("Enter Image URL: ")
        # Default for testing
        if not image_input:
            image_input = "https://upload.wikimedia.org/wikipedia/commons/a/a9/Adidas_Sneaker.jpg"
            print(f"Using default: {image_input}")
    
    elif choice == "2":
        image_input = input("Enter local path (e.g., product.jpg): ")
        is_url = False
        if not os.path.exists(image_input):
            print("Error: File not found.")
            return
    else:
        print("Invalid choice.")
        return

    # Run Analysis
    result = analyze_image(image_input, is_url)
    
    if result:
        print("\n" + "="*60)
        print("✨ ANALYSIS RESULT")
        print("="*60)
        print(f"📦 TITLE:       {result.title}")
        print(f"📂 CATEGORY:    {result.estimated_category}")
        print(f"👀 CONDITION:   {result.visual_condition}")
        print("-" * 30)
        print(f"📝 DESCRIPTION: {result.description}")
        print("-" * 30)
        print(f"⭐ FEATURES:    {', '.join(result.features)}")
        print(f"🏷️ TAGS:        {', '.join(result.tags)}")
        print("="*60)
        
        # Option to save
        save = input("\nSave to file? (y/n): ")
        if save.lower() == 'y':
            with open("product_listing.txt", "w", encoding="utf-8") as f:
                f.write(f"Title: {result.title}\nDescription: {result.description}\nTags: {result.tags}")
            print("Saved to product_listing.txt")

if __name__ == "__main__":
    main()
