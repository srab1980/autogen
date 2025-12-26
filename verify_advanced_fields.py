import sqlite3
import json
import os

DB_PATH = "autogen04202.db"

def dump_model():
    if not os.path.exists(DB_PATH):
        print(f"Database {DB_PATH} not found.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get the gpt-5.2 model from gallery
    cursor.execute("SELECT id, config FROM gallery WHERE id = 3")
    row = cursor.fetchone()
    
    if row:
        config = json.loads(row[1])
        print("=== OpenAI gpt-5.2 Configuration ===")
        print(json.dumps(config, indent=2))
        
        # Extract and show the config fields specifically
        if 'config' in config:
            cfg = config['config']
            print("\n=== Model Configuration Fields ===")
            print(f"model: {cfg.get('model')}")
            print(f"organization: {cfg.get('organization')}")
            print(f"base_url: {cfg.get('base_url')}")
            print(f"timeout: {cfg.get('timeout')}")
            print(f"max_retries: {cfg.get('max_retries')}")
            print(f"temperature: {cfg.get('temperature')}")
            print(f"max_tokens: {cfg.get('max_tokens')}")
            print(f"top_p: {cfg.get('top_p')}")
            print(f"frequency_penalty: {cfg.get('frequency_penalty')}")
            print(f"presence_penalty: {cfg.get('presence_penalty')}")
            print(f"stop: {cfg.get('stop')}")
    
    conn.close()

if __name__ == "__main__":
    dump_model()
