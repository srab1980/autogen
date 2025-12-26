import sqlite3
import json
import os

DB_PATH = "autogen04202.db"

def inspect():
    if not os.path.exists(DB_PATH):
        print(f"Database {DB_PATH} not found.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Look for a model in gallery
    cursor.execute("SELECT id, config FROM gallery")
    for row_id, blob in cursor.fetchall():
        config = json.loads(blob)
        if config.get('component_type') == 'model' or 'model' in config.get('config', {}):
            print(f"=== MODEL ID {row_id} ===")
            print(json.dumps(config, indent=2))
            # Just show one for now
            break
            
    conn.close()

if __name__ == "__main__":
    inspect()
