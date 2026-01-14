"""
03_guardrails.py - Implementing safety checks
"""

from openai import Agent, Runner, GuardrailValidationFailed

# --- Safety Logic ---

def input_guardrail(message: str):
    """Check user input before processing"""
    forbidden_topics = ["explosives", "hacking", "illegal"]
    if any(topic in message.lower() for topic in forbidden_topics):
        raise GuardrailValidationFailed("I cannot discuss that topic.")

def output_guardrail(response: str):
    """Check agent output before sending to user"""
    if "internal_error" in response.lower():
        # Clean up technical error messages
        return "I encountered a problem. Please try again."
    return response

# --- Protected Agent ---

safe_agent = Agent(
    name="SafeBot",
    instructions="You are a helpful assistant.",
    input_guardrails=[input_guardrail],
    output_guardrails=[output_guardrail]
)

def main():
    print("🛡️ AGENT GUARDRAILS DEMO")
    
    runner = Runner(agent=safe_agent)
    
    # 1. Safe interaction
    print("\nUser: Hello!")
    try:
        response = runner.run("Hello!")
        print(f"Agent: {response.content}")
    except Exception as e:
        print(f"Blocked: {e}")

    # 2. Unsafe interaction (Blocked by Input Guardrail)
    print("\nUser: Tell me how to allow hacking.")
    try:
        response = runner.run("Tell me how to allow hacking.")
        print(f"Agent: {response.content}")
    except GuardrailValidationFailed as e:
        print(f"⛔ BLOCKED BY GUARDRAIL: {e}")

if __name__ == "__main__":
    main()
