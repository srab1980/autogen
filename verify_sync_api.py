import requests
import json
import time

BASE_URL = "http://localhost:8081/api"
USER_ID = "guestuser@gmail.com"  # Default user ID usually

def get_gallery(user_id):
    response = requests.get(f"{BASE_URL}/gallery/?user_id={user_id}")
    response.raise_for_status()
    data = response.json()
    if data['status'] and data['data']:
        return data['data'][0]
    return None

def create_team(team_config):
    response = requests.post(f"{BASE_URL}/teams/", json=team_config)
    response.raise_for_status()
    return response.json()['data']

def get_team(team_id, user_id):
    response = requests.get(f"{BASE_URL}/teams/{team_id}?user_id={user_id}")
    response.raise_for_status()
    return response.json()['data']

def update_team(team_config):
    response = requests.post(f"{BASE_URL}/teams/", json=team_config)
    response.raise_for_status()
    return response.json()['data']

def update_gallery(gallery_id, gallery_config, user_id):
    # API requires PUT with the data
    response = requests.put(f"{BASE_URL}/gallery/{gallery_id}?user_id={user_id}", json=gallery_config)
    response.raise_for_status()
    return response.json()['data']

def run_test():
    print("Fetching Gallery...")
    gallery = get_gallery(USER_ID)
    if not gallery:
        print("No gallery found!")
        return

    gallery_id = gallery['id']
    # Pick the first agent
    agent_in_gallery = gallery['config']['components']['agents'][0]
    agent_id = agent_in_gallery.get('id') or agent_in_gallery.get('client_id')
    
    # If agent has no ID (common in default gallery), assign one and update gallery first
    if not agent_id:
        import uuid
        agent_id = str(uuid.uuid4())
        agent_in_gallery['id'] = agent_id
        # Update gallery with ID
        gallery['config']['components']['agents'][0] = agent_in_gallery
        print(f"Assigning ID {agent_id} to agent and updating gallery...")
        res = requests.put(f"{BASE_URL}/gallery/{gallery_id}?user_id={USER_ID}", json=gallery)
        res.raise_for_status()
        gallery = res.json()['data'] # Assuming the gallery update returns the full gallery object in 'data'
        agent_in_gallery = gallery['config']['components']['agents'][0] # Re-get agent from updated gallery

    print(f"Testing with Agent: {agent_in_gallery.get('label')} (ID: {agent_id})")

    # Simulate Frontend: Create Team with this agent + _origin metadata
    origin_data = {
        "gallery_id": gallery_id,
        "component_id": agent_id, # Use the potentially newly assigned agent_id
        "component_type": "agent"
    }
    
    # Deep copy agent config to avoid mutating original for now
    agent_for_team = json.loads(json.dumps(agent_in_gallery))
    if "metadata" not in agent_for_team:
        agent_for_team["metadata"] = {}
    # IMPORTANT: config.metadata values must be strings in AssistantAgentConfig
    agent_for_team["metadata"]["_origin"] = json.dumps(origin_data)

    team_payload = {
        "user_id": USER_ID,
        "component": {
            "name": "SyncTestTeam",
            "participants": [agent_for_team],
            "admin_name": "Admin",
            "messages": []
        }
    }

    print("Creating Team...")
    team = create_team(team_payload)
    team_id = team['id']
    print(f"Team Created (ID: {team_id})")

    # --- Test 1: Team Update -> Gallery Sync ---
    print("\n--- Test 1: Updating Team to sync to Gallery ---")
    new_description = f"Updated via Team at {time.time()}"
    team['component']['participants'][0]['description'] = new_description
    
    print(f"Setting Agent Description in Team to: '{new_description}'")
    update_team(team)
    
    # Check Gallery
    print("Fetching Gallery to verify sync...")
    updated_gallery = get_gallery(USER_ID)
    updated_agent = next(a for a in updated_gallery['config']['components']['agents'] if (a.get('id') == agent_id or a.get('client_id') == agent_id))
    
    if updated_agent['description'] == new_description:
        print("SUCCESS: Gallery updated from Team change!")
    else:
        print(f"FAILURE: Gallery description '{updated_agent['description']}' != '{new_description}'")

    # --- Test 2: Gallery Update -> Team Sync ---
    print("\n--- Test 2: Updating Gallery to sync to Team ---")
    gallery_desc = f"Updated via Gallery at {time.time()}"
    updated_agent['description'] = gallery_desc
    
    # Need to preserve the whole gallery structure
    updated_gallery['config']['components']['agents'][0] = updated_agent # Assuming index 0 still
    
    print(f"Setting Agent Description in Gallery to: '{gallery_desc}'")
    update_gallery(gallery_id, updated_gallery, USER_ID)
    
    # Check Team
    print("Fetching Team to verify sync...")
    updated_team = get_team(team_id, USER_ID)
    team_agent_desc = updated_team['component']['participants'][0]['description']
    
    if team_agent_desc == gallery_desc:
        print("SUCCESS: Team updated from Gallery change!")
    else:
        print(f"FAILURE: Team description '{team_agent_desc}' != '{gallery_desc}'")

    # Cleanup
    # requests.delete(f"{BASE_URL}/teams/{team_id}?user_id={USER_ID}")

if __name__ == "__main__":
    try:
        run_test()
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        if e.response is not None:
            print(f"Response: {e.response.text}")
    except Exception as e:
        print(f"Unexpected Error: {e}")
