# 🕵️ Project 1: Auto Researcher

## 📝 Overview

In this project, we will build an **Autonomous Research Agent**. This agent takes a complex topic (e.g., "The future of solid-state batteries in EVs") and performs a deep research task.

Instead of just answering with one prompt, it uses the **o1-preview (reasoning)** model to:
1.  **Plan**: Break down the topic into sub-questions.
2.  **Execute**: "Search" (simulated) for information on each sub-question.
3.  **Synthesize**: Combine all findings into a structured report.

### Key Concepts
- **Reasoning Models (`o1`)**: How to leverage models that "think" before they speak.
- **Chain of Thought**: Explicitly formulating a plan.
- **Structured Output**: Ensuring the final report follows a strict format.

---

## 🏗️ Step-by-Step Implementation

### Step 1: Define the Research Plan Structure

First, we need to define *what* our agent should produce. We want a list of sub-questions to research.

```python
from pydantic import BaseModel, Field
from typing import List

class ResearchPlan(BaseModel):
    main_topic: str
    sub_questions: List[str] = Field(description="List of 3-5 specific questions to research")
    market_focus: str = Field(description="The primary industry or market this research targets")
```

### Step 2: Create the "Planner" Function

We use `gpt-4o` or `gpt-5-mini` to generate this plan. Note that for simple planning, `gpt-4o` is excellent.

### Step 3: The "Reseacher" Loop (Using `o1`)

This is where the magic happens. We will use the `o1-preview` or `o1-mini` model. These models excel at complex reasoning. We'll ask it to take a sub-question and provide a detailed analysis.

> **Note**: `o1` models currently (as of 2026) work best with straightforward prompts and high `reasoning_effort`. They don't support system messages in the traditional way (they use "developer messages" or just user messages).

### Step 4: Synthesis

Finally, we combine the `o1` outputs into a final report.

---

## 💻 The Code

The complete code is available in `app.py`.

### How to Run

1.  Make sure you have your API key set:
    ```bash
    set OPENAI_API_KEY=sk-...
    ```
2.  Install requirements:
    ```bash
    pip install openai pydantic
    ```
3.  Run the researcher:
    ```bash
    python app.py
    ```

### Expected Output

You will see the agent:
1.  Generates a plan (e.g., "1. Current State...", "2. Key Challenges...").
2.  "Thinking..." about each question.
3.  Prints a final markdown report.

---

## 🧠 Challenge for You

**Extend this project**:
1.  **Add Real Search**: Integrate a search tool (like Tavily or Bing Search) so the agent fetches *real* live data instead of using its internal knowledge.
2.  **Save to PDF**: Use a library like `fpdf` or `markdown-pdf` to save the final report as a PDF file.
