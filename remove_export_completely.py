"""
COMPLETELY REMOVE the export tool from rafeeq_exporter
The workflow will work and user runs export script manually after
"""
import sqlite3
import json

DB_PATH = "autogen04202.db"

def remove_all_tools():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("=== REMOVING ALL EXPORT TOOLS ===")
    
    cursor.execute("SELECT id, component FROM team WHERE id = 4")
    row = cursor.fetchone()
    config = json.loads(row[1])
    
    participants = config.get('config', {}).get('participants', [])
    
    for participant in participants:
        agent_name = participant.get('config', {}).get('name', '')
        
        # Remove workbench from exporter too
        if 'workbench' in participant.get('config', {}):
            del participant['config']['workbench']
            print(f"  ✗ Removed workbench from {agent_name}")
    
    cursor.execute("UPDATE team SET component = ? WHERE id = ?", 
                  (json.dumps(config), 4))
    conn.commit()
    
    # Verify
    cursor.execute("SELECT component FROM team WHERE id = 4")
    new_config = cursor.fetchone()[0]
    if 'export_to_word' in new_config or 'para' in new_config:
        print("\n⚠️ WARNING: Still found export/para in config!")
    else:
        print("\n✅ Clean! No export tools or 'para' in config.")
    
    conn.close()

if __name__ == "__main__":
    remove_all_tools()
