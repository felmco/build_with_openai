# Module 9: Production Deployment

## 📋 Module Overview

**Duration**: 4 hours
**Level**: Advanced
**Prerequisites**: Module 8 (Advanced Topics)

Moving from a prototype to production requires a different mindset. This module covers the essential "Day 2" operations: Security, Observability, Cost Management, and Reliability.

---

## 🎯 Learning Objectives

- ✅ Secure your AI application (API Key management, Injection prevention).
- ✅ Implement robust **Monitoring and Logging**.
- ✅ Estimate and optimize **Token Costs**.
- ✅ Handle Rate Limits gracefully at scale.

---

## 📖 Table of Contents

1. [Security Best Practices](#1-security)
2. [Monitoring & Logging](#2-monitoring)
3. [Cost Optimization](#3-cost)

---

## 1. Security Best Practices

AI apps have unique vulnerabilities, such as Prompt Injection.

[➡️ Checklist: 01_security_checklist.md](./01_security_checklist.md)

**Key Rules**:
1.  Never commit API keys.
2.  Validate all inputs (even to agents).
3.  Sanitize outputs (guardrails).
4.  Use least-privilege API keys (Project-scoped).

---

## 2. Monitoring & Logging

You need to know what your users are asking and how the model is responding.

[➡️ Code Example: 02_monitoring_logging.py](./02_monitoring_logging.py)

We simulate a logging middleware that captures:
- Latency (Time to First Token)
- Token Usage (Prompt vs Completion)
- Error Rates

---

## 3. Cost Optimization

Start with the best model, then optimize.

[➡️ Code Example: 03_cost_estimator.py](./03_cost_estimator.py)

**Strategies**:
- **Model Waterfall**: Try `gpt-5-mini` first, fall back to `gpt-4o` only if needed.
- **Caching**: Don't pay for the same answer twice.
- **Batch API**: 50% discount for non-urgent tasks.

---

## 📚 Resources

- [OpenAI Production Best Practices](https://platform.openai.com/docs/guides/production-best-practices)
- [OWASP Top 10 for LLMs](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
