"""
09_function_calling.py - Use functions as tools
"""

import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()


def get_current_weather(location, unit="celsius"):
    """Get the current weather in a given location"""
    # Mock API call
    weather_info = {
        "location": location,
        "temperature": "22",
        "unit": unit,
        "forecast": ["sunny", "windy"]
    }
    return json.dumps(weather_info)


def run_conversation():
    print("\n" + "="*60)
    print("FUNCTION CALLING")
    print("="*60)

    # Step 1: Define tools
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA",
                        },
                        "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                    },
                    "required": ["location"],
                },
            },
        }
    ]

    # Step 2: Send conversation + tools to model
    messages = [{"role": "user", "content": "What's the weather like in Boston?"}]
    
    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    # Step 3: Check if model wanted to call a function
    if tool_calls:
        print(f"Tool calls detected: {len(tool_calls)}")
        
        # Extend conversation with assistant's reply
        messages.append(response_message)

        available_functions = {
            "get_current_weather": get_current_weather,
        }

        # Step 4: Execute function calls
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            
            print(f"Calling function: {function_name} with args: {function_args}")
            
            function_response = function_to_call(
                location=function_args.get("location"),
                unit=function_args.get("unit"),
            )
            
            # Step 5: Send function result back to model
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )

        # Step 6: Get final response
        second_response = client.chat.completions.create(
            model="gpt-5-mini",
            messages=messages
        )
        
        print(f"\nFinal Response: {second_response.choices[0].message.content}")


def main():
    run_conversation()


if __name__ == "__main__":
    main()
