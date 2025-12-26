import sqlite3
import json

conn = sqlite3.connect('autogen04202.db')
cursor = conn.cursor()

# List tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("Tables:", [t[0] for t in tables])

# Check team table
cursor.execute("SELECT id, component FROM team LIMIT 5")
rows = cursor.fetchall()

for row in rows:
    team_id = row[0]
    try:
        component = json.loads(row[1])
        model_client = None
        
        # Check participants for model_client
        if 'config' in component and 'participants' in component['config']:
            for agent in component['config']['participants']:
                if 'config' in agent and 'model_client' in agent['config']:
                    mc = agent['config']['model_client']
                    print(f"\nTeam {team_id} - Agent: {agent.get('label', 'unknown')}")
                    print(f"  Model: {mc.get('config', {}).get('model', 'N/A')}")
                    print(f"  Model Info: {mc.get('config', {}).get('model_info', 'NOT SET')}")
    except Exception as e:
        print(f"Error parsing team {team_id}: {e}")

conn.close()
