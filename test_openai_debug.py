"""
Test OpenAI with debugging enabled
"""
import logging
logging.basicConfig(level=logging.DEBUG)

import httpx
from openai import OpenAI

API_KEY = "sk-proj-REDACTED"

print("=== Testing with debug logging ===")
try:
    client = OpenAI(api_key=API_KEY, timeout=30.0)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Hi"}],
        max_tokens=5
    )
    print(f"Success: {response.choices[0].message.content}")
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
