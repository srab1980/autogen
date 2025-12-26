import requests
import json
import os

# Check if port 8081 is open? Assume yes since previous context said so.
url = "http://127.0.0.1:8081/api/gallery?user_id=guestuser"
print(f"Fetching from {url}...")

try:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    
    # Save to file
    with open("api_gallery_response.json", "w") as f:
        json.dump(data, f, indent=2)
        
    print(f"Response saved to api_gallery_response.json")
    print(f"Response status code: {response.status_code}")
    print(f"Number of galleries: {len(data)}")
    
    if len(data) > 0:
        gallery = data[0]
        print(f"First Gallery ID: {gallery.get('id')}")
        components = gallery.get("config", {}).get("components", {})
        agents = components.get("agents", [])
        print(f"Number of agents: {len(agents)}")
        
        for agent in agents:
            if agent.get("label") == "AssistantAgent":
                model_client = agent.get("config", {}).get("model_client", {})
                version = agent.get("version")
                model_client_version = model_client.get("version")
                print(f"AssistantAgent Version: {version}")
                print(f"AssistantAgent Model Client Version: {model_client_version}")
                
except Exception as e:
    print(f"Error calling API: {e}")
