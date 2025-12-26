import sqlite3
import json
import os
from dotenv import dotenv_values

DB_PATH = 'autogen04202.db'

MODEL_INFO_51 = {
    "vision": True,
    "function_calling": True,
    "json_output": True,
    "family": "gpt-5",
    "structured_output": True,
    "multiple_system_messages": True
}

MODEL_INFO_52 = {
    "vision": True,
    "function_calling": True,
    "json_output": True,
    "family": "gpt-5",
    "structured_output": True,
    "multiple_system_messages": True
}

def get_api_key():
    config = dotenv_values(".env")
    for key, value in config.items():
        if key == 'OPENAI_API_KEY' and value and value.startswith('sk-proj-'):
            return value
    return config.get('OPENAI_API_KEY')

def fix_recursive(node, api_key):
    modified = False
    if isinstance(node, dict):
        # 1. Revert gpt-5.1 if label matches
        if node.get('label') == 'OpenAI gpt-5.1' or node.get('description') == 'OpenAI gpt-5.1':
            config = node.get('config', {})
            if isinstance(config, dict):
                if config.get('model') != 'gpt-5.1':
                    print("  Reverting model to gpt-5.1 for component: " + node.get('label', 'Unknown'))
                    config['model'] = 'gpt-5.1'
                    config['api_key'] = api_key
                    config['model_info'] = MODEL_INFO_51
                    modified = True

        # 2. General model_client fix (ensure API key and model_info)
        elif 'model_client' in node:
            mc = node['model_client']
            if isinstance(mc, dict) and 'config' in mc:
                cfg = mc['config']
                if cfg.get('model') == 'gpt-5.1':
                    if cfg.get('api_key') != api_key or 'model_info' not in cfg:
                        print("  Updating API key/info for nested gpt-5.1")
                        cfg['api_key'] = api_key
                        cfg['model_info'] = MODEL_INFO_51
                        modified = True

        for key, value in node.items():
            if fix_recursive(value, api_key):
                modified = True
    elif isinstance(node, list):
        for item in node:
            if fix_recursive(item, api_key):
                modified = True
    return modified

def apply():
    api_key = get_api_key()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Update existing
    for table, col in [('team', 'component'), ('gallery', 'config')]:
        print(f"Processing {table}...")
        cursor.execute(f"SELECT id, {col} FROM {table}")
        for row_id, blob in cursor.fetchall():
            if not blob: continue
            data = json.loads(blob)
            if fix_recursive(data, api_key):
                print(f"  Saving changes to {table} ID {row_id}")
                cursor.execute(f"UPDATE {table} SET {col} = ? WHERE id = ?", (json.dumps(data), row_id))
    
    # Add GPT-5.2 to Gallery if not exists
    cursor.execute("SELECT count(*) FROM gallery WHERE config LIKE '%gpt-5.2%'")
    if cursor.fetchone()[0] == 0:
        print("Adding OpenAI gpt-5.2 to Gallery...")
        new_model_config = {
            "provider": "autogen_ext.models.openai.OpenAIChatCompletionClient",
            "component_type": "model",
            "version": 1,
            "component_version": 1,
            "description": "OpenAI gpt-5.2",
            "label": "OpenAI gpt-5.2",
            "config": {
                "model": "gpt-5.2",
                "api_key": api_key,
                "model_info": MODEL_INFO_52
            }
        }
        cursor.execute("INSERT INTO gallery (config) VALUES (?)", (json.dumps(new_model_config),))
    
    conn.commit()
    conn.close()
    print("Branding and expansion complete.")

if __name__ == "__main__":
    apply()
