import sqlite3
import json
import os

DB_PATH = 'autogen04202.db'

from dotenv import dotenv_values

def get_api_key():
    config = dotenv_values(".env")
    # Priority 1: Real sk-proj key
    for key, value in config.items():
        if key == 'OPENAI_API_KEY' and value and value.startswith('sk-proj-'):
            return value
    # Priority 2: Any non-placeholder sk- key
    for key, value in config.items():
        if key == 'OPENAI_API_KEY' and value and value.startswith('sk-') and not value.startswith('sk-...'):
            return value
    return config.get('OPENAI_API_KEY')

def update_model_config(node, api_key):
    updated = False
    if isinstance(node, dict):
        # Check if this node is a model configuration
        # AutoGen Studio models often have 'model' and 'api_key' in their config
        if 'model' in node and 'api_key' in node:
            print(f"  Updating key for model: {node['model']}")
            node['api_key'] = api_key
            updated = True
        
        # Also check model_client structures
        if 'model_client' in node:
            mc = node['model_client']
            if isinstance(mc, dict) and 'config' in mc:
                if 'api_key' in mc['config']:
                    print(f"  Updating model_client key for model: {mc['config'].get('model')}")
                    mc['config']['api_key'] = api_key
                    updated = True

        # Recurse
        for key, value in node.items():
            if update_model_config(value, api_key):
                updated = True
    elif isinstance(node, list):
        for item in node:
            if update_model_config(item, api_key):
                updated = True
    return updated

def main():
    api_key = get_api_key()
    if not api_key:
        print("Error: OPENAI_API_KEY not found in .env")
        return
    
    # Check if the key is just a placeholder or too short
    if len(api_key) < 10 or api_key.startswith('sk-proj-REDACTED'):
        print(f"Warning: API Key looks invalid: {api_key}")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    tables_to_fix = [
        ('team', 'component'),
        ('gallery', 'config'),
    ]

    for table, column in tables_to_fix:
        print(f"Processing table: {table}")
        cursor.execute(f"SELECT id, {column} FROM {table}")
        rows = cursor.fetchall()
        
        for row_id, blob in rows:
            if not blob:
                continue
            try:
                data = json.loads(blob)
                if update_model_config(data, api_key):
                    print(f"  Updating {table} ID {row_id}")
                    cursor.execute(f"UPDATE {table} SET {column} = ? WHERE id = ?", (json.dumps(data), row_id))
            except Exception as e:
                print(f"  Error processing {table} ID {row_id}: {e}")

    conn.commit()
    conn.close()
    print("Database model keys updated.")

if __name__ == "__main__":
    main()
