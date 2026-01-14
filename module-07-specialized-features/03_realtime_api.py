"""
03_realtime_api.py - Multimodal WebSockets
"""

import asyncio
import json
import os
# Requires: pip install websockets
import websockets

API_KEY = os.getenv("OPENAI_API_KEY")
URL = "wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview-2024-10-01"

async def realtime_session():
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "OpenAI-Beta": "realtime=v1"
    }
    
    print(f"🔌 Connecting to Realtime API: {URL}")
    
    async with websockets.connect(URL, extra_headers=headers) as ws:
        print("✅ Connected. Sending session update...")
        
        # 1. Configure the session (e.g., voice settings)
        await ws.send(json.dumps({
            "type": "session.update",
            "session": {
                "modalities": ["text", "audio"],
                "voice": "alloy"
            }
        }))
        
        # 2. Receive events loop
        # In a real app, you would send audio bytes here concurrently
        
        # Send a text message to trigger response
        await ws.send(json.dumps({
            "type": "conversation.item.create",
            "item": {
                "type": "message",
                "role": "user",
                "content": [{"type": "input_text", "text": "Hello! tell me a joke."}]
            }
        }))
        await ws.send(json.dumps({"type": "response.create"}))
        
        print("👂 Listening for response events...")
        try:
            async for message in ws:
                event = json.loads(message)
                event_type = event.get("type")
                
                if event_type == "response.text.delta":
                    print(event["delta"], end="", flush=True)
                elif event_type == "response.done":
                    print("\n[Response Complete]")
                    break
        except Exception as e:
            print(f"Error: {e}")

def main():
    print("⚡ REALTIME API DEMO")
    print("="*60)
    if not API_KEY:
        print("Error: OPENAI_API_KEY not set.")
        return
        
    try:
        asyncio.run(realtime_session())
    except ImportError:
        print("Please install 'websockets': pip install websockets")

if __name__ == "__main__":
    main()
