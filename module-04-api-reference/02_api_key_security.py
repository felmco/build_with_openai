"""
02_api_key_security.py - API key security patterns
"""

import os
from dotenv import load_dotenv
from pathlib import Path


class SecureAPIKeyManager:
    """Secure API key management"""

    def __init__(self, env_path=".env"):
        self.env_path = Path(env_path)

    def load_key(self):
        """Load key from environment variable"""
        load_dotenv(self.env_path)
        key = os.getenv("OPENAI_API_KEY")
        
        if not key:
            raise ValueError("API key not found in environment variables")
        
        if not key.startswith("sk-"):
            raise ValueError("Invalid API key format")
            
        return key

    def rotate_key(self, new_key):
        """Simulate key rotation"""
        # In a real app, this would update a secrets manager (e.g., AWS Secrets Manager, Vault)
        print(f"Rotating API key to: {new_key[:8]}...")
        # update_secrets_manager(new_key)


def main():
    manager = SecureAPIKeyManager()
    
    try:
        key = manager.load_key()
        print(f"Successfully loaded key: {key[:8]}..." + "*"*20)
        
        # Simulate rotation
        manager.rotate_key("sk-new-rotated-key-12345")
        
    except Exception as e:
        print(f"Security Error: {e}")


if __name__ == "__main__":
    main()
