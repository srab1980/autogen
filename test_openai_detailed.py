"""
Test OpenAI client with explicit configuration
"""
import httpx
from openai import OpenAI

API_KEY = "sk-proj-REDACTED"

print("=== Test 1: Normal OpenAI client ===")
try:
    client = OpenAI(api_key=API_KEY)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Say hi"}],
        max_tokens=10
    )
    print(f"Success: {response.choices[0].message.content}")
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")

print("\n=== Test 2: OpenAI client with explicit http_client ===")
try:
    http_client = httpx.Client(timeout=60.0)
    client = OpenAI(api_key=API_KEY, http_client=http_client)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Say hi"}],
        max_tokens=10
    )
    print(f"Success: {response.choices[0].message.content}")
    http_client.close()
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")

print("\n=== Test 3: OpenAI client with explicit timeout ===")
try:
    client = OpenAI(api_key=API_KEY, timeout=60.0)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Say hi"}],
        max_tokens=10
    )
    print(f"Success: {response.choices[0].message.content}")
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")
