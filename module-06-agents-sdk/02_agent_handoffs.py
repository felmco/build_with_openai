"""
02_agent_handoffs.py - Multi-agent orchestration
"""

from enum import Enum
from openai import Agent, Runner, Handoff

# --- Specialized Agents ---

class FlightBookingAgent(Agent):
    def __init__(self):
        super().__init__(
            name="Flight Booker",
            instructions="You help users book flights. Ask for destination and dates.",
            tools=[self.search_flights]
        )
    
    def search_flights(self, destination: str, date: str) -> str:
        """Search for flights"""
        return f"Found flights to {destination} on {date}: AA123, UA456."

class HotelBookingAgent(Agent):
    def __init__(self):
        super().__init__(
            name="Hotel Booker",
            instructions="You help users book hotels. Ask for city and preferences.",
            tools=[self.search_hotels]
        )

    def search_hotels(self, city: str) -> str:
        """Search for hotels"""
        return f"Found hotels in {city}: Marriott, Hilton."

# --- Triage Agent ---

def transfer_to_flights():
    """Transfer user to the flight booking specialist"""
    return Handoff(agent=FlightBookingAgent())

def transfer_to_hotels():
    """Transfer user to the hotel booking specialist"""
    return Handoff(agent=HotelBookingAgent())

triage_agent = Agent(
    name="Triage",
    instructions="You are the main receptionist. Direct users to the right department.",
    tools=[transfer_to_flights, transfer_to_hotels]
)

# --- Main Runtime ---

def main():
    print("🏨 TRAVEL AGENCY SYSTEM (Multi-Agent)")
    
    runner = Runner(agent=triage_agent)
    
    # Trace the active agent
    print(f"Current Agent: {runner.current_agent.name}")
    
    # 1. User wants flights
    print("\nUser: I need to fly to Paris.")
    response = runner.run("I need to fly to Paris.")
    print(f"Agent ({runner.current_agent.name}): {response.content}")
    
    # Notice the runner automatically switched context to Flight Booker
    if runner.current_agent.name == "Flight Booker":
        print("✅ Successfully handed off to Flight Booker")

    # 2. Continue conversation in new context
    print("\nUser: On June 1st.")
    response = runner.run("On June 1st.")
    print(f"Agent ({runner.current_agent.name}): {response.content}")

if __name__ == "__main__":
    main()
