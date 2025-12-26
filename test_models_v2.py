"""
Test gpt-5.x models without max_tokens (they may not support it)
"""
import os
os.environ['HTTP_PROXY'] = ''
os.environ['HTTPS_PROXY'] = ''
os.environ['OPENAI_BASE_URL'] = 'https://api.openai.com/v1'

from openai import OpenAI

API_KEY = "sk-proj-REDACTED"

models_to_test = ['gpt-4o-mini', 'gpt-5.1', 'gpt-5.2']

client = OpenAI(api_key=API_KEY, timeout=60.0)

for model in models_to_test:
    print(f"\n=== Testing {model} ===")
    try:
        # Don't use max_tokens for gpt-5.x models
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Say 'hello' and nothing else"}]
        )
        print(f"✅ SUCCESS: {response.choices[0].message.content}")
    except Exception as e:
        print(f"❌ ERROR: {type(e).__name__}: {e}")
