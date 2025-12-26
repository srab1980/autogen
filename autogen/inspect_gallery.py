import asyncio
import os
from autogenstudio.database import DatabaseManager
from autogenstudio.datamodel import Gallery

HOME = os.path.expanduser("~")
APP_DIR = os.path.join(HOME, ".autogenstudio")
DB_URI = f"sqlite:///{os.path.join(APP_DIR, 'database.sqlite')}"

async def main():
    print(f"Connecting to DB at {DB_URI}")
    db_manager = DatabaseManager(engine_uri=DB_URI, base_dir=APP_DIR)
    
    print("--- Gallery ---")
    gallery_res = db_manager.get(Gallery, return_json=True)
    if gallery_res.status:
        print(f"Found {len(gallery_res.data)} galleries.")
        for gallery in gallery_res.data:
            print(f"  ID: {gallery['id']}")
            config = gallery.get('config', {})
            components = config.get('components', {})
            agents = components.get('agents', [])
            print(f"    Agents: {len(agents)}")
            for agent in agents:
                print(f"      - {agent.get('label') or agent.get('name')}")
    else:
        print(f"Failed to get galleries: {gallery_res.message}")

if __name__ == "__main__":
    asyncio.run(main())
