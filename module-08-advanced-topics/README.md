# Module 8: Advanced Topics

## 📋 Module Overview

**Duration**: 6 hours
**Level**: Advanced
**Prerequisites**: Module 6 (Agents SDK)

This module is for engineers who need to push the boundaries of LLM performance. We cover how to get the most out of **Reasoning Models (`o1`)**, how to scientifically measure performance with **Evals**, and advanced prompting strategies.

---

## 🎯 Learning Objectives

- ✅ Master **Reasoning Models** (o1, o1-mini) for complex problem solving.
- ✅ Implement **Chain of Thought** and other advanced prompting techniques.
- ✅ Build an **Evaluation Framework** to test your AI application.
- ✅ Understand **Prompt Optimization**.

---

## 📖 Table of Contents

1. [Advanced Prompting Strategies](#1-prompting)
2. [Reasoning Models Deep Dive](#2-reasoning)
3. [Building Evaluations (Evals)](#3-evals)

---

## 1. Advanced Prompting Strategies

We go beyond "You are a helper". We explore:
- **Chain of Thought (CoT)**
- **Few-Shot Prompting**
- **Meta-Prompting** (Asking the model to improve the prompt)

[➡️ Code Example: 01_advanced_prompting.py](./01_advanced_prompting.py)

---

## 2. Reasoning Models Deep Dive

The `o1` series models work differently. They "think" before they speak. This section covers when to use them and how to structure inputs for maximum reasoning effort.

[➡️ Code Example: 03_reasoning_deep_dive.py](./03_reasoning_deep_dive.py)

**Best Practices**:
- Simpler prompts often work better (less "guidance").
- Use delimiters clearly.
- Give the model space to think.

---

## 3. Building Evaluations (Evals)

You can't improve what you don't measure. We build a simple framework to score model outputs against a "Gold Standard".

[➡️ Code Example: 02_evals_framework.py](./02_evals_framework.py)

```python
score = evaluate(
    generated_answer="The capital is Paris.",
    expected_answer="Paris",
    metric="exact_match"
)
```

---

## 📚 Resources

- [OpenAI Evals Github](https://github.com/openai/evals)
- [Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
