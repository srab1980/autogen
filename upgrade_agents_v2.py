import sqlite3
import json

def upgrade_agents_to_v2(config, path="root"):
    """Recursively upgrade all agents to version 2 and ensure workbench is an array"""
    changes = []
    
    if isinstance(config, dict):
        # Check if this is an agent
        if config.get('component_type') == 'agent':
            agent_name = config.get('config', {}).get('name', config.get('label', 'unknown'))
            current_version = config.get('component_version', 1)
            
            # Upgrade version to 2
            if current_version < 2:
                config['version'] = 2
                config['component_version'] = 2
                changes.append(f"Upgraded {agent_name} from v{current_version} to v2")
            
            # Ensure workbench is an array
            agent_config = config.get('config', {})
            if 'workbench' in agent_config:
                wb = agent_config['workbench']
                if isinstance(wb, dict):
                    agent_config['workbench'] = [wb]
                    changes.append(f"  - Converted workbench to array for {agent_name}")
        
        # Recursively process
        for key, value in config.items():
            if isinstance(value, (dict, list)):
                changes.extend(upgrade_agents_to_v2(value, f"{path}.{key}"))
    
    elif isinstance(config, list):
        for i, item in enumerate(config):
            changes.extend(upgrade_agents_to_v2(item, f"{path}[{i}]"))
    
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
    
    changes = upgrade_agents_to_v2(config)
    
    if changes:
        print("\n".join(changes))
        
        # Update database
        new_config = json.dumps(config, ensure_ascii=False)
        cursor.execute("UPDATE team SET component = ? WHERE id = ?", (new_config, team_id))
        print(f"  Updated in database\n")
    else:
        print("  No changes needed\n")

conn.commit()
conn.close()

print("Done!")
