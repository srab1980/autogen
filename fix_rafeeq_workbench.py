import sqlite3
import json

def fix_workbench(config):
    """Recursively fix workbench fields to be arrays instead of single objects"""
    fixed = False
    
    if isinstance(config, dict):
        # Check if this is an agent with a workbench that's a dict (not a list)
        if 'config' in config and isinstance(config.get('config'), dict):
            agent_config = config['config']
            if 'workbench' in agent_config:
                wb = agent_config['workbench']
                if isinstance(wb, dict):
                    # Convert single workbench object to array
                    agent_config['workbench'] = [wb]
                    print(f"  Fixed workbench for agent: {agent_config.get('name', 'unknown')}")
                    fixed = True
        
        # Also check for participants array
        if 'participants' in config:
            for participant in config.get('participants', []):
                if fix_workbench(participant):
                    fixed = True
        
        # Recursively process all nested dicts
        for key, value in config.items():
            if isinstance(value, (dict, list)):
                if fix_workbench(value):
                    fixed = True
    
    elif isinstance(config, list):
        for item in config:
            if fix_workbench(item):
                fixed = True
    
    return fixed

# Connect to database
conn = sqlite3.connect('autogen04202.db')
cursor = conn.cursor()

# Get the Rafeeq team
cursor.execute("SELECT id, component FROM team WHERE id = 2")
row = cursor.fetchone()

if row:
    team_id = row[0]
    config = json.loads(row[1])
    
    print(f"Processing team ID {team_id}: {config.get('label', 'unknown')}")
    print()
    
    # Fix workbench fields
    if fix_workbench(config):
        # Update the database
        new_config = json.dumps(config, ensure_ascii=False)
        cursor.execute("UPDATE team SET component = ? WHERE id = ?", (new_config, team_id))
        conn.commit()
        print(f"\nDatabase updated successfully!")
        
        # Save fixed config for verification
        with open('rafeeq_team_config_fixed.json', 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print("Saved fixed config to rafeeq_team_config_fixed.json")
    else:
        print("No workbench fixes needed")

conn.close()
