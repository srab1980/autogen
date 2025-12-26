import sqlite3
import json
import os
from dotenv import dotenv_values

DB_PATH = 'autogen04202.db'

DEFAULT_MODEL_INFO = {
    "vision": True,
    "function_calling": True,
    "json_output": True,
    "family": "gpt-5",
    "structured_output": True,
    "multiple_system_messages": True
}

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

def fix_recursive(node, api_key):
    modified = False
    if isinstance(node, dict):
        # Look for model_client blocks
        if node.get('component_type') == 'model' or 'model_client' in node or ('model' in node and 'provider' in node):
            # If it's a model config or has a model client
            config = node.get('config', {})
            if isinstance(config, dict):
                # If it has a 'model' field, it's likely a model config
                if 'model' in config:
                    if config.get('api_key') != api_key:
                        print(f"  Injecting/Updating key for model: {config.get('model')}")
                        config['api_key'] = api_key
                        modified = True
                    
                    # Also ensure model_info for gpt-5.1
                    if config.get('model') == 'gpt-5.1':
                        if not config.get('model_info'):
                            print(f"  Adding model_info for gpt-5.1")
                            config['model_info'] = DEFAULT_MODEL_INFO
                            modified = True
            
            # Recurse into model_client if it exists
            if 'model_client' in node:
                if fix_recursive(node['model_client'], api_key):
                    modified = True

        # Always recurse into all dict values
        for key, value in node.items():
            if fix_recursive(value, api_key):
                modified = True
                
    elif isinstance(node, list):
        for item in node:
            if fix_recursive(item, api_key):
                modified = True
                
    return modified

def apply_fix():
    api_key = get_api_key()
    if not api_key:
        print("No API key found!")
        return
    
    print(f"Using API Key: {api_key[:15]}...")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Tables to check
    targets = [('team', 'component'), ('gallery', 'config')]
    
    for table, col in targets:
        print(f"Processing table: {table}")
        cursor.execute(f"SELECT id, {col} FROM {table}")
        rows = cursor.fetchall()
        for row_id, blob in rows:
            if not blob: continue
            try:
                data = json.loads(blob)
                if fix_recursive(data, api_key):
                    print(f"  Updating {table} ID {row_id}")
                    new_blob = json.dumps(data)
                    cursor.execute(f"UPDATE {table} SET {col} = ? WHERE id = ?", (new_blob, row_id))
            except Exception as e:
                print(f"  Error processing {table} ID {row_id}: {e}")
                
    conn.commit()
    conn.close()
    print("Database patch complete.")

if __name__ == "__main__":
    apply_fix()
