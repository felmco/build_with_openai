# 👁️ Project 2: Vision Sales Assistant

## 📝 Overview

In this project, we utilize the multimodal capabilities of **GPT-4o** to analyze product images. The goal is to build a tool that takes an image url (or file) and automatically generates:

1.  **Product Title**: Optimized for SEO.
2.  **Description**: Engaging marketing copy.
3.  **Keywords**: Relevant tags for search visibility.
4.  **Price Estimate**: A rough estimate based on visual characteristics (demonstrating reasoning).

### Key Concepts
- **GPT-4o Vision**: How to send images to the model.
- **Multimodal Prompting**: Combining text and image inputs.
- **Structured JSON Output**: Forcing the model to return data in a specific format for our app.

---

## 🏗️ Step-by-Step Implementation

### Step 1: Define the Output Structure

We don't want a blob of text; we want structured data we can save to a database.

```python
from pydantic import BaseModel, Field
from typing import List

class ProductAnalysis(BaseModel):
    title: str = Field(description="SEO optimized product title")
    description: str = Field(description="Engaging marketing description")
    tags: List[str] = Field(description="5-10 relevant keywords")
    category: str
    visual_condition: str = Field(description="New, Used, Refurbished, etc.")
```

### Step 2: The Vision Pipeline

We use the standard Chat Completions API, but with a twist: the `messages` content includes an `image_url` type.

```python
messages=[
    {
        "role": "user",
        "content": [
            {"type": "text", "text": "Analyze this product image..."},
            {"type": "image_url", "image_url": {"url": image_url}}
        ]
    }
]
```

### Step 3: Handling Local Images

To send a local image, you need to base64 encode it first. We included a helper function `encode_image` in the full code to handle this.

---

## 💻 The Code

The complete code is available in `app.py`.

### How to Run

1.  Install requirements:
    ```bash
    pip install openai pydantic requests
    ```
2.  Run the assistant:
    ```bash
    python app.py
    ```
3.  Enter an image URL when prompted. You can try these examples:
    -   *Sneaker*: `https://upload.wikimedia.org/wikipedia/commons/a/a9/Adidas_Sneaker.jpg`
    -   *Smart Watch*: `https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_Watch_Series_5_Space_Gray_Aluminum_Case_with_Black_Sport_Band_-_44mm.png`

### Expected Output

The script will output a nicely formatted JSON-like structure:

```json
{
  "title": "Adidas Originals Classic Sneaker - Blue/White",
  "description": "Step up your style game with these iconic Adidas sneakers...",
  "tags": ["adidas", "sneakers", "footwear", "casual", "blue"],
  ...
}
```

---

## 🧠 Challenge for You

**Extend this project**:
1.  **Bulk Processing**: Modify the script to iterate over a folder of images.
2.  **Social Media Mode**: Add a prompt parameter to generate captions specifically for Instagram (with hashtags) vs LinkedIn (professional).
