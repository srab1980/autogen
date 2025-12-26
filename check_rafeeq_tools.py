import sqlite3
import json

conn = sqlite3.connect('autogen04202.db')
cursor = conn.cursor()

# Find Rafeeq2 team
cursor.execute("SELECT id, component FROM team")
for team_id, blob in cursor.fetchall():
    config = json.loads(blob)
    label = config.get('label', '')
    if 'rafeeq' in label.lower():
        print(f"=== Team {team_id}: {label} ===")
        
        # Look for tools
        def find_tools(obj, path=""):
            if isinstance(obj, dict):
                if obj.get('component_type') == 'tool':
                    print(f"  Tool at {path}: {obj.get('label', 'NO LABEL')}")
                    if 'source_code' in obj.get('config', {}):
                        print(f"    Source: {obj['config']['source_code'][:200]}...")
                for k, v in obj.items():
                    find_tools(v, f"{path}.{k}")
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    find_tools(item, f"{path}[{i}]")
        
        find_tools(config)
        
        # Save full config
        with open(f"rafeeq_team_{team_id}.json", "w", encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print(f"\n  Full config saved to rafeeq_team_{team_id}.json")

conn.close()
