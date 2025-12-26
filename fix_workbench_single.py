import sqlite3
import json

def fix_workbench_to_single(config, path="root"):
    """Recursively convert workbench arrays back to single objects"""
    changes = []
    
    if isinstance(config, dict):
        # Check if this is an agent with a workbench array
        if config.get('component_type') == 'agent':
            agent_config = config.get('config', {})
            agent_name = agent_config.get('name', config.get('label', 'unknown'))
            
            if 'workbench' in agent_config:
                wb = agent_config['workbench']
                if isinstance(wb, list):
                    if len(wb) == 1:
                        # Convert single-item array to object
                        agent_config['workbench'] = wb[0]
                        changes.append(f"Converted workbench from array to single object for: {agent_name}")
                    elif len(wb) == 0:
                        # Remove empty workbench array
                        del agent_config['workbench']
                        changes.append(f"Removed empty workbench array for: {agent_name}")
                    else:
                        # Multiple workbenches - take the first one (backend only supports one)
                        agent_config['workbench'] = wb[0]
                        changes.append(f"WARNING: Multiple workbenches for {agent_name}, using first one only")
        
        # Recursively process
        for key, value in config.items():
            if isinstance(value, (dict, list)):
                changes.extend(fix_workbench_to_single(value, f"{path}.{key}"))
    
    elif isinstance(config, list):
        for i, item in enumerate(config):
            changes.extend(fix_workbench_to_single(item, f"{path}[{i}]"))
    
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
    
    changes = fix_workbench_to_single(config)
    
    if changes:
        for change in changes:
            print(f"  {change}")
        
        # Update database
        new_config = json.dumps(config, ensure_ascii=False)
        cursor.execute("UPDATE team SET component = ? WHERE id = ?", (new_config, team_id))
        print(f"  Updated in database\n")
    else:
        print("  No changes needed\n")

conn.commit()
conn.close()

print("Done!")
