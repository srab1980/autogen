import sqlite3
import json

DB_PATH = 'autogen04202.db'

def fix_model_names(node):
    modified = False
    if isinstance(node, dict):
        if 'model' in node and node['model'] == 'gpt-5.1':
            print("  Replacing gpt-5.1 with gpt-4o-mini")
            node['model'] = 'gpt-4o-mini'
            modified = True
        
        for key, value in node.items():
            if fix_model_names(value):
                modified = True
    elif isinstance(node, list):
        for item in node:
            if fix_model_names(item):
                modified = True
    return modified

def apply():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    for table, col in [('team', 'component'), ('gallery', 'config')]:
        print(f"Checking {table}...")
        cursor.execute(f"SELECT id, {col} FROM {table}")
        for row_id, blob in cursor.fetchall():
            if not blob: continue
            data = json.loads(blob)
            if fix_model_names(data):
                print(f"  Updating {table} ID {row_id}")
                cursor.execute(f"UPDATE {table} SET {col} = ? WHERE id = ?", (json.dumps(data), row_id))
    
    conn.commit()
    conn.close()
    print("Model name normalization complete.")

if __name__ == "__main__":
    apply()
