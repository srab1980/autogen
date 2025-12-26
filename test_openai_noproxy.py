"""
Test OpenAI with proxy bypass
"""
import os
import httpx
from openai import OpenAI

# Force disable proxy
os.environ['HTTP_PROXY'] = ''
os.environ['HTTPS_PROXY'] = ''
os.environ['http_proxy'] = ''
os.environ['https_proxy'] = ''
os.environ['NO_PROXY'] = '*'

API_KEY = "sk-proj-REDACTED"

print("=== Test with proxy disabled ===")
try:
    # Create a custom http client with no proxy
    http_client = httpx.Client(
        timeout=60.0,
        proxy=None  # Explicitly disable proxy
    )
    client = OpenAI(api_key=API_KEY, http_client=http_client)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "What is 2+2? Reply with just the number."}],
        max_tokens=10
    )
    print(f"SUCCESS! Response: {response.choices[0].message.content}")
    http_client.close()
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
