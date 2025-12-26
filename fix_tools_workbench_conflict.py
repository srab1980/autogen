import sqlite3
import json

def remove_tools_if_workbench(config, path="root"):
    """Remove 'tools' field from agents that have a workbench"""
    changes = []
    
    if isinstance(config, dict):
        # Check if this is an agent
        if config.get('component_type') == 'agent':
            agent_config = config.get('config', {})
            agent_name = agent_config.get('name', config.get('label', 'unknown'))
            
            # If agent has both tools and workbench, remove tools
            has_workbench = 'workbench' in agent_config and agent_config['workbench']
            has_tools = 'tools' in agent_config and agent_config['tools']
            
            if has_workbench and has_tools:
                del agent_config['tools']
                changes.append(f"Removed 'tools' from {agent_name} (has workbench)")
        
        # Recursively process
        for key, value in config.items():
            if isinstance(value, (dict, list)):
                changes.extend(remove_tools_if_workbench(value, f"{path}.{key}"))
    
    elif isinstance(config, list):
        for i, item in enumerate(config):
            changes.extend(remove_tools_if_workbench(item, f"{path}[{i}]"))
    
    return changes

# Connect to database
conn = sqlite3.connect('autogen04202.db')
cursor = conn.cursor()

# Get all teams
cursor.execute("SELECT id, component FROM team")
rows = cursor.fetchall()

print(f"Found {len(rows)} teams\n")

for row in rows:
    team_id = row[0]
    config = json.loads(row[1])
    team_name = config.get('label', 'unknown')
    
    print(f"Processing team {team_id}: {team_name}")
    
    changes = remove_tools_if_workbench(config)
    
    if changes:
        for change in changes:
            print(f"  {change}")
        
        new_config = json.dumps(config, ensure_ascii=False)
        cursor.execute("UPDATE team SET component = ? WHERE id = ?", (new_config, team_id))
        print(f"  Updated in database\n")
    else:
        print("  No changes needed\n")

conn.commit()
conn.close()

print("Done!")
