"""
02_monitoring_logging.py - Observability pattern
"""

import time
import logging
import json
from openai import OpenAI

# Configure structured logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("ai_monitor")

client = OpenAI()

def log_interaction(event_type, duration_ms, tokens_in, tokens_out, model, status="success"):
    """
    Structured log entry for observability tools (Datadog, Splunk, etc.)
    """
    event = {
        "event": event_type,
        "status": status,
        "duration_ms": round(duration_ms, 2),
        "model": model,
        "token_usage": {
            "prompt": tokens_in,
            "completion": tokens_out,
            "total": tokens_in + tokens_out
        },
        "cost_estimate": estimate_cost(model, tokens_in, tokens_out)
    }
    logger.info(json.dumps(event))

def estimate_cost(model, prompt_tok, comp_tok):
    # Hypothetical 2026 pricing
    rates = {
        "gpt-5-mini": {"in": 0.15/1000000, "out": 0.60/1000000},
        "gpt-4o":    {"in": 2.50/1000000, "out": 10.00/1000000}
    }
    rate = rates.get(model, rates["gpt-5-mini"])
    return (prompt_tok * rate["in"]) + (comp_tok * rate["out"])

def safe_chat_completion(prompt):
    start = time.time()
    model = "gpt-5-mini"
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        duration = (time.time() - start) * 1000
        
        usage = response.usage
        log_interaction(
            "chat_completion", 
            duration, 
            usage.prompt_tokens, 
            usage.completion_tokens, 
            model
        )
        return response.choices[0].message.content
        
    except Exception as e:
        duration = (time.time() - start) * 1000
        log_interaction("chat_completion", duration, 0, 0, model, status=f"error: {str(e)}")
        return "Sorry, I encountered an error."

def main():
    print("📊 MONITORING DEMO (Check logs)")
    response = safe_chat_completion("Hello, how are you?")
    print(f"Response: {response}")

if __name__ == "__main__":
    main()
