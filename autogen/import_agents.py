import asyncio
import os
import json
from pathlib import Path
from autogenstudio.database import DatabaseManager

# Paths
HOME = os.path.expanduser("~")
APP_DIR = os.path.join(HOME, ".autogenstudio")
DB_URI = f"sqlite:///{os.path.join(APP_DIR, 'database.sqlite')}"

# User ID
USER_ID = "guestuser@gmail.com"

# JSON files
WORKSPACE = r"c:\Users\srab1\Downloads\AutoGen Studio\AutoGen Studio\autogen"
TRAVEL_TEAM = os.path.join(WORKSPACE, r"python\packages\autogen-studio\notebooks\travel_team.json")
TEAM = os.path.join(WORKSPACE, r"python\packages\autogen-studio\notebooks\team.json")

async def main():
    print(f"Connecting to DB at {DB_URI}")
    # Ensure app dir exists
    if not os.path.exists(APP_DIR):
        print(f"App directory {APP_DIR} does not exist. Creating...")
        os.makedirs(APP_DIR, exist_ok=True)
        
    db_manager = DatabaseManager(engine_uri=DB_URI, base_dir=APP_DIR)
    
    # Initialize to ensure tables exist if not already
    print("Initializing database...")
    init_res = db_manager.initialize_database()
    print(f"Init result: {init_res.message}")

    files = [TRAVEL_TEAM, TEAM]
    
    for fpath in files:
        if os.path.exists(fpath):
            print(f"Importing {fpath}...")
            try:
                result = await db_manager.import_team(team_config=fpath, user_id=USER_ID, check_exists=True)
                print(f"Result for {os.path.basename(fpath)}: {result.message}, Status: {result.status}")
                if result.status and result.data:
                    print(f"  ID: {result.data.get('id')}")
            except Exception as e:
                print(f"Error importing {fpath}: {e}")
        else:
            print(f"File not found: {fpath}")

if __name__ == "__main__":
    asyncio.run(main())
