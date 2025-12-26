import sqlite3
import json

conn = sqlite3.connect('autogen04202.db')
c = conn.cursor()

# Get the Rafeeq team (row ID 2)
c.execute("SELECT component FROM team WHERE id = 2")
row = c.fetchone()

if row:
    component_json = row[0]
    data = json.loads(component_json)
    
    # Save to file for easier viewing
    with open('rafeeq_team_config.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print("Saved full config to rafeeq_team_config.json")
    
    # Look for participants/agents with workbench
    participants = data.get('config', {}).get('participants', [])
    print(f"\nNumber of participants: {len(participants)}")
    
    for i, p in enumerate(participants):
        name = p.get('config', {}).get('name', 'unknown')
        wb = p.get('config', {}).get('workbench')
        print(f"\n--- Agent {i}: {name} ---")
        print(f"Provider: {p.get('provider')}")
        print(f"Workbench type: {type(wb)}")
        if wb:
            print(f"Workbench: {json.dumps(wb, indent=2)[:1000]}")

conn.close()
