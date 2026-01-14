"""
04_agent_patterns.py - Common architectural patterns
"""

from openai import Agent, Runner

# ==========================================
# Pattern 1: Orchestrator-Workers
# ==========================================
# Use Case: Complex task decomposition
# Structure: One "Brain" agent breaks down a task and assigns to "Worker" agents.

def pattern_orchestrator():
    print("\n🎭 Pattern: Orchestrator-Workers")
    
    # Workers
    coder = Agent(name="Coder", instructions="Write Python code.")
    reviewer = Agent(name="Reviewer", instructions="Check code for bugs.")
    
    # Orchestrator
    orchestrator = Agent(
        name="Tech Lead",
        instructions="""
        You manage a dev team.
        1. Ask Coder to write the solution.
        2. Ask Reviewer to check it.
        3. Compile the final answer.
        """,
        # In a real scenario, tools would call these sub-agents
        tools=[
            lambda task: f"Coder Output: def solve(): pass", # Simulated
            lambda code: f"Reviewer Output: LGTM"             # Simulated
        ]
    )
    
    print("Orchestrator: Delegating tasks...")
    # runner.run("Build a login page")

# ==========================================
# Pattern 2: Evaluator-Optimizer
# ==========================================
# Use Case: High quality output generation (iterative refinement)
# Structure: Generator -> Evaluator -> (Loop if not good enough) -> Final

def pattern_evaluator_optimizer():
    print("\n🔄 Pattern: Evaluator-Optimizer")
    
    generator = Agent(name="Writer", instructions="Write a short story.")
    evaluator = Agent(name="Editor", instructions="Rate the story 1-10 and give feedback.")
    
    topic = "A robot learning to love."
    
    # Simulation of the loop
    current_draft = "Robot saw flower. Robot felt fuzzy."
    print(f"Draft 1: {current_draft}")
    
    feedback = "Too simple. Needs more emotion. Score: 4/10" # from Evaluator
    print(f"Feedback: {feedback}")
    
    current_draft = "Unit 734 processed the visual input of the rose. A strange warmth spread through its circuits..."
    print(f"Draft 2: {current_draft}")
    
    feedback = "Excellent. Score: 9/10"
    print(f"Final: {current_draft}")


# ==========================================
# Pattern 3: Parallelization
# ==========================================
# Use Case: Speed / Independent sub-tasks
# Structure: Run multiple agents at the same time and aggregate results.

def pattern_parallel():
    print("\n⚡ Pattern: Parallelization")
    
    # Task: Analyze a company
    # Agent A: Financial Analysis
    # Agent B: Market Analysis
    # Agent C: Competitor Analysis
    
    print("Launching constraints agents simultaneously...")
    # results = await asyncio.gather(agent_a.run(), agent_b.run(), agent_c.run())
    print("Aggregating results into final report.")


def main():
    print("AGENT ARCHITECTURE PATTERNS")
    print("="*60)
    
    pattern_orchestrator()
    pattern_evaluator_optimizer()
    pattern_parallel()

if __name__ == "__main__":
    main()
