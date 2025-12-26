import os
from dotenv import dotenv_values
import requests

def test_key():
    config = dotenv_values(".env")
    api_key = None
    
    # Let's find the sk-proj key specifically
    for key, value in config.items():
        if key == 'OPENAI_API_KEY':
            print(f"Found key in .env: {key}={value[:15]}...")
            if value.startswith('sk-proj-'):
                api_key = value
                
    if not api_key:
        api_key = config.get('OPENAI_API_KEY')
        
    print(f"Using API Key for test: {api_key[:15]}...")
    
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    try:
        response = requests.get("https://api.openai.com/v1/models", headers=headers, timeout=10)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("Successfully connected to OpenAI!")
            # print(f"Models: {[m['id'] for m in response.json()['data'][:3]]}")
        else:
            print(f"Error Response: {response.text}")
    except Exception as e:
        print(f"Connection Error: {e}")

if __name__ == "__main__":
    test_key()
