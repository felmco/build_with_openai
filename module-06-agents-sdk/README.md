# Module 6: Building Agents with the Agents SDK

## 📋 Module Overview

**Duration**: 3 hours
**Level**: Advanced
**Prerequisites**: Module 5 (Platform APIs)

In 2025, OpenAI introduced the **Agents SDK**, a powerful Python-first framework for building autonomous AI systems. This module covers how to move beyond simple chatbots to complex, multi-agent systems that can plan, execute, and collaborate.

> **Note**: This replaces the deprecated "Assistants API" path.

---

## 🎯 Learning Objectives

- ✅ Understand the **Agents SDK** architecture (Agents, Runners, Handoffs).
- ✅ Build a **Single Agent** that uses tools.
- ✅ Implement **Multi-Agent Systems** using Handoffs.
- ✅ Apply **Guardrails** for safety and control.
- ✅ Master common **Agent Patterns** (Orchestrator-Workers, Evaluator-Optimizer).

---

## 📖 Table of Contents

1. [The Agents SDK Concepts](#1-concepts)
2. [Building Your First Agent](#2-first-agent)
3. [Multi-Agent Systems (Handoffs)](#3-handoffs)
4. [Agent Patterns](#4-patterns)
5. [Safety & Guardrails](#5-guardrails)

---

## 1. The Agents SDK Concepts

The SDK introduces a few core primitives:
- **Agent**: The cognitive entity with instructions, model, and tools.
- **Handouff**: A mechanism for one agent to transfer the conversation to another.
- **Runner**: The execution loop that manages the conversation state and tool calling.

---

## 2. Building Your First Agent

We start with a simple agent that has a tool.

[➡️ Code Example: 01_simple_agent.py](./01_simple_agent.py)

```python
from openai import Agent

agent = Agent(
    name="Math Helper",
    instructions="You are a helpful math tutor.",
    tools=[calculator_tool]
)
```

---

## 3. Multi-Agent Systems (Handoffs)

The real power comes when agents work together. Instead of one giant prompt, we split responsibilities.

[➡️ Code Example: 02_agent_handoffs.py](./02_agent_handoffs.py)

**The Pattern**:
1. **Triage Agent**: Listens to user request.
2. **Handoff**: Transfers to specialized agent (e.g., `FlightBookingAgent`).
3. **Execution**: Specialized agent completes task.
4. **Return**: Optionally hands back to triage or ends.

---

## 4. Agent Patterns

We explore standard architectural patterns for robust AI systems.

[➡️ Code Example: 04_agent_patterns.py](./04_agent_patterns.py)

### Common Patterns:
1.  **Orchestrator-Workers**: A central brain breaks down a task and delegates to sub-agents.
2.  **Evaluator-Optimizer**: One agent generates a solution, another critiques it, and the first improves it loop.
3.  **Parallelization**: Running multiple agents simultaneously on sub-tasks.

---

## 5. Safety & Guardrails

Production agents need safety checks. The SDK allows "Guardrail Functions" that run before or after the LLM.

[➡️ Code Example: 03_guardrails.py](./03_guardrails.py)

---

## 📚 Resources

- [Official Agents SDK Documentation](https://platform.openai.com/docs/agents)
- [OpenAI Cookbook - Agents](https://cookbook.openai.com/)
