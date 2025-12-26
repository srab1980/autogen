"""
Diagnose OpenAI connection issues
"""
import os
import sys

print("=== Environment Variables ===")
for key in ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy', 'NO_PROXY', 'SSL_CERT_FILE']:
    value = os.environ.get(key)
    if value:
        print(f"{key}: {value}")

print("\n=== Testing with httpx (what OpenAI uses) ===")
import httpx

API_KEY = "sk-proj-REDACTED"

try:
    # Test with httpx directly
    response = httpx.get(
        "https://api.openai.com/v1/models",
        headers={"Authorization": f"Bearer {API_KEY}"},
        timeout=30.0
    )
    print(f"httpx Status: {response.status_code}")
except Exception as e:
    print(f"httpx Error: {type(e).__name__}: {e}")

print("\n=== Testing with requests ===")
import requests

try:
    response = requests.get(
        "https://api.openai.com/v1/models",
        headers={"Authorization": f"Bearer {API_KEY}"},
        timeout=30
    )
    print(f"requests Status: {response.status_code}")
except Exception as e:
    print(f"requests Error: {type(e).__name__}: {e}")
