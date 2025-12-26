"""
Test the OpenAI connection using the exact same configuration as Team 1
"""
import asyncio
from openai import OpenAI

# Configuration from Team 1
API_KEY = "sk-proj-REDACTED"
MODEL = "gpt-4o-mini"

def test_direct():
    print(f"Testing model: {MODEL}")
    print(f"API Key: {API_KEY[:20]}...")
    
    client = OpenAI(api_key=API_KEY)
    
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": "What is the capital of France? Reply in one word."}],
            max_tokens=50
        )
        print(f"Success! Response: {response.choices[0].message.content}")
    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}")

if __name__ == "__main__":
    test_direct()
