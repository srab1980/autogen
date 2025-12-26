import asyncio
import os
from autogenstudio.database import DatabaseManager
from autogenstudio.datamodel import Team, Agent

HOME = os.path.expanduser("~")
APP_DIR = os.path.join(HOME, ".autogenstudio")
DB_URI = f"sqlite:///{os.path.join(APP_DIR, 'database.sqlite')}"

async def main():
    print(f"Connecting to DB at {DB_URI}")
    db_manager = DatabaseManager(engine_uri=DB_URI, base_dir=APP_DIR)
    
    print("--- Teams ---")
    teams_res = db_manager.get(Team, return_json=True)
    if teams_res.status:
        print(f"Found {len(teams_res.data)} teams.")
        for team in teams_res.data:
            print(f"  ID: {team['id']}, User: {team['user_id']}")
    else:
        print(f"Failed to get teams: {teams_res.message}")

    print("\n--- Agents ---")
    agents_res = db_manager.get(Agent, return_json=True)
    if agents_res.status:
        print(f"Found {len(agents_res.data)} agents.")
        for agent in agents_res.data:
            print(f"  ID: {agent['id']}, User: {agent['user_id']}")
    else:
        print(f"Failed to get agents: {agents_res.message}")

if __name__ == "__main__":
    asyncio.run(main())
