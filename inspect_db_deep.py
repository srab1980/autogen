import sqlite3
import json

DB_PATH = 'autogen04202.db'

def inspect():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("=== MODELS IN GALLERY ===")
    cursor.execute("SELECT id, config FROM gallery")
    for row_id, blob in cursor.fetchall():
        config = json.loads(blob)
        if config.get('component_type') == 'model' or config.get('provider') == 'autogen_core.models.OpenAIChatCompletionClient':
            print(f"ID {row_id}: {config.get('label')} -> {config.get('config', {}).get('model')}")
            print(f"  API KEY: {config.get('config', {}).get('api_key', 'MISSING')[:10]}...")
            print(f"  BASE URL: {config.get('config', {}).get('base_url', 'DEFAULT')}")
        
    print("\n=== TEAMS ===")
    cursor.execute("SELECT id, component FROM team")
    for row_id, blob in cursor.fetchall():
        print(f"TEAM ID {row_id} (first 500 chars of config):")
        print(blob[:500])
        print("-" * 20)
        
    conn.close()

if __name__ == "__main__":
    inspect()
