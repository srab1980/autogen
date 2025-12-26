import sqlite3
import json
import os
from dotenv import dotenv_values

DB_PATH = "autogen04202.db"

DEFAULT_MODEL_INFO = {
    "vision": True,
    "function_calling": True,
    "json_output": True,
    "family": "gpt-5",
    "structured_output": True,
    "multiple_system_messages": True
}

# List of custom model names that need model_info
CUSTOM_MODELS = ['gpt-5.1', 'gpt-5.2', 'OpenAI gpt-5.1', 'OpenAI gpt-5.2']

def fix_model_info(obj):
    """Recursively add model_info to custom models"""
    modified = False
    
    if isinstance(obj, dict):
        if 'config' in obj and isinstance(obj['config'], dict):
            cfg = obj['config']
            if 'model' in cfg:
                model_name = cfg.get('model')
                
                # Check if this is a custom model that needs model_info
                if model_name in CUSTOM_MODELS or model_name.startswith('gpt-5'):
                    if 'model_info' not in cfg or cfg['model_info'] is None:
                        print(f"  Adding model_info to: {model_name}")
                        cfg['model_info'] = DEFAULT_MODEL_INFO
                        modified = True
        
        # Recurse into all nested dicts
        for key, value in obj.items():
            if fix_model_info(value):
                modified = True
    
    elif isinstance(obj, list):
        for item in obj:
            if fix_model_info(item):
                modified = True
    
    return modified

def main():
    if not os.path.exists(DB_PATH):
        print(f"Database {DB_PATH} not found.")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Fix Gallery entries
    print("=== FIXING GALLERY MODELS ===")
    cursor.execute("SELECT id, config FROM gallery")
    gallery_rows = cursor.fetchall()
    
    for row_id, blob in gallery_rows:
        config = json.loads(blob)
        
        if config.get('component_type') == 'model' or 'model' in config.get('config', {}):
            print(f"\nGallery ID {row_id}: {config.get('label')}")
            
            if fix_model_info(config):
                cursor.execute("UPDATE gallery SET config = ? WHERE id = ?", 
                             (json.dumps(config), row_id))
                print(f"  ✓ Fixed")
            else:
                print(f"  → Already has model_info")
    
    # Fix Team entries
    print("\n=== FIXING TEAM MODELS ===")
    cursor.execute("SELECT id, component FROM team")
    team_rows = cursor.fetchall()
    
    for team_id, blob in team_rows:
        config = json.loads(blob)
        print(f"\nTeam ID {team_id}")
        
        if fix_model_info(config):
            cursor.execute("UPDATE team SET component = ? WHERE id = ?", 
                         (json.dumps(config), team_id))
            print(f"  ✓ Fixed")
        else:
            print(f"  → Already has model_info")
    
    conn.commit()
    conn.close()
    
    print("\n✅ All models now have model_info!")

if __name__ == "__main__":
    main()
