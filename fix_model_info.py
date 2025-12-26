import sqlite3
import json

conn = sqlite3.connect('autogen04202.db')
cursor = conn.cursor()

# Define model_info for unknown models
DEFAULT_MODEL_INFO = {
    "vision": True,
    "function_calling": True,
    "json_output": True,
    "family": "gpt-5",
    "structured_output": True,
    "multiple_system_messages": True
}

# Get all teams
cursor.execute("SELECT id, component FROM team")
rows = cursor.fetchall()

updates = []
for row in rows:
    team_id = row[0]
    modified = False
    try:
        component = json.loads(row[1])
        
        # Check participants for model_client
        if 'config' in component and 'participants' in component['config']:
            for agent in component['config']['participants']:
                if 'config' in agent and 'model_client' in agent['config']:
                    mc = agent['config']['model_client']
                    model_name = mc.get('config', {}).get('model', '')
                    model_info = mc.get('config', {}).get('model_info')
                    
                    # If model_info is missing or null, add it
                    if not model_info:
                        print(f"Team {team_id} - Fixing model '{model_name}' (adding model_info)")
                        mc['config']['model_info'] = DEFAULT_MODEL_INFO
                        modified = True
        
        if modified:
            updates.append((json.dumps(component), team_id))
            
    except Exception as e:
        print(f"Error parsing team {team_id}: {e}")

# Apply updates
for component_json, team_id in updates:
    cursor.execute("UPDATE team SET component = ? WHERE id = ?", (component_json, team_id))
    print(f"Updated team {team_id}")

conn.commit()
print(f"\nTotal teams updated: {len(updates)}")
conn.close()
