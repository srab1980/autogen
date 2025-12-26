"""
Test various OpenAI configurations to find what works
"""
import os
import ssl
import httpx

# Clear proxy settings
os.environ['HTTP_PROXY'] = ''
os.environ['HTTPS_PROXY'] = ''
os.environ['http_proxy'] = ''
os.environ['https_proxy'] = ''

API_KEY = "sk-proj-REDACTED"

print("=== Test 1: Direct httpx POST (simulating OpenAI call) ===")
try:
    response = httpx.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": "Hi"}],
            "max_tokens": 5
        },
        timeout=30.0
    )
    print(f"Success! Status: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")

print("\n=== Test 2: Using OPENAI_BASE_URL env var ===")
os.environ['OPENAI_BASE_URL'] = 'https://api.openai.com/v1'
try:
    from openai import OpenAI
    client = OpenAI(api_key=API_KEY)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Hi"}],
        max_tokens=5
    )
    print(f"Success! Response: {response.choices[0].message.content}")
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")
