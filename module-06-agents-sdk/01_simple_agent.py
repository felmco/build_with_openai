"""
01_simple_agent.py - Your first agent using the Agents SDK
"""

# Hypothetical Import in 2026
from openai import Agent, Runner

# Define tools
def calculator(a: int, b: int, operation: str) -> int:
    """Performs basic arithmetic operations."""
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    return 0

def main():
    print("🤖 SIMPLE AGENT DEMO")

    # 1. Define the Agent
    # Agents are stateful entities with defined capabilities.
    math_agent = Agent(
        name="Math Tutor",
        model="gpt-4o-mini",
        instructions="You are a helpful tutor. Use the calculator tool to answer questions. Explain your steps.",
        tools=[calculator]
    )

    # 2. Run the Agent
    # The Runner manages the loop: User -> Agent -> Tools -> Agent -> User
    print(f"Chatting with {math_agent.name} (Type 'quit' to exit)")
    
    runner = Runner(agent=math_agent)
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['quit', 'exit']:
            break
            
        print(f"{math_agent.name}: ", end="", flush=True)
        
        # Stream the response
        result = runner.run(user_input)
        print(result.content)
        
        # In a real SDK, you might inspect tool calls:
        # if result.tool_calls:
        #    print(f"[Debug] Used tools: {result.tool_calls}")

if __name__ == "__main__":
    main()
