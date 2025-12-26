import asyncio
import os
import json
from autogenstudio.database import DatabaseManager
from autogenstudio.datamodel import Gallery, GalleryConfig, GalleryMetadata, GalleryComponents

# Paths
HOME = os.path.expanduser("~")
APP_DIR = os.path.join(HOME, ".autogenstudio")
DB_URI = f"sqlite:///{os.path.join(APP_DIR, 'database.sqlite')}"
USER_ID = "guestuser@gmail.com"

# JSON files
WORKSPACE = r"c:\Users\srab1\Downloads\AutoGen Studio\AutoGen Studio\autogen"
TRAVEL_TEAM = os.path.join(WORKSPACE, r"python\packages\autogen-studio\notebooks\travel_team.json")
TEAM = os.path.join(WORKSPACE, r"python\packages\autogen-studio\notebooks\team.json")

def extract_agents_from_team(team_path):
    agents = []
    if not os.path.exists(team_path):
        print(f"File not found: {team_path}")
        return agents
        
    with open(team_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    # Check for participants in config
    participants = data.get('config', {}).get('participants', [])
    for p in participants:
        # Ensure it's an agent definition
        if p.get('component_type') == 'agent':
            # Override label with name if available to make it distinct in UI
            name = p.get('config', {}).get('name')
            if name:
                p['label'] = name
            agents.append(p)
            print(f"Extracted agent: {p.get('label')}")
            
    return agents

async def main():
    print(f"Connecting to DB at {DB_URI}")
    db_manager = DatabaseManager(engine_uri=DB_URI, base_dir=APP_DIR)
    
    all_agents = []
    all_agents.extend(extract_agents_from_team(TEAM))
    all_agents.extend(extract_agents_from_team(TRAVEL_TEAM))
    
    print(f"Total extracted agents: {len(all_agents)}")
    
    if not all_agents:
        print("No agents to import.")
        return

    # Create or Get Gallery
    gallery_id = "default_gallery" # Use a distinct ID
    
    # Try to fetch existing gallery (though checking inspecting result said 0)
    # We will just create a new one to be sure
    
    gallery_config = GalleryConfig(
        id=gallery_id,
        name="Imported Agents Gallery",
        metadata=GalleryMetadata(
            author="autogen-studio",
            version="1.0.0",
            description="Gallery containing agents extracted from team configurations."
        ),
        components=GalleryComponents(
            agents=all_agents,
            models=[],
            tools=[],
            terminations=[],
            teams=[],
            workbenches=[]
        )
    )
    
    gallery = Gallery(
        id=1, 
        user_id=USER_ID,
        config=gallery_config.model_dump()
    )
    
    # We need to handle ID carefully. If we upsert with ID=None, it creates new. 
    # Let's search if any gallery exists first.
    existing_galleries_res = db_manager.get(Gallery)
    if existing_galleries_res.status and existing_galleries_res.data:
        print("Found existing galleries, updating the first one...")
        existing_gallery = existing_galleries_res.data[0]
        # Merge agents
        current_config = existing_gallery.config
        if isinstance(current_config, dict):
             # Depending on how it return (dict vs object)
             # The inspect_gallery script showed it returns object if return_json=False
             pass 
        
        # Simplified approach: Since we found 0 galleries, we just create one.
    
    print("Upserting gallery...")
    res = db_manager.upsert(gallery)
    print(f"Gallery upsert result: {res.message}, Status: {res.status}")

if __name__ == "__main__":
    asyncio.run(main())
