import sqlite3
import json
import os

DB_PATH = "autogen04202.db"

DEFAULT_MODEL_INFO = {
    "vision": True,
    "function_calling": True,
    "json_output": True,
    "family": "gpt-5",
    "structured_output": True,
    "multiple_system_messages": True
}

def check_model_info():
    if not os.path.exists(DB_PATH):
        print(f"Database {DB_PATH} not found.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("=== CHECKING GALLERY MODELS ===")
    cursor.execute("SELECT id, config FROM gallery")
    for row_id, blob in cursor.fetchall():
        config = json.loads(blob)
        if config.get('component_type') == 'model' or 'model' in config.get('config', {}):
            cfg = config.get('config', {})
            model_name = cfg.get('model', 'UNKNOWN')
            model_info = cfg.get('model_info')
            
            print(f"\nGallery ID {row_id}: {config.get('label')}")
            print(f"  Model: {model_name}")
            print(f"  Has model_info: {model_info is not None}")
            
            if model_info is None:
                print(f"  ⚠️ MISSING model_info!")
    
    print("\n=== CHECKING TEAM MODELS ===")
    cursor.execute("SELECT id, component FROM team")
    for team_id, blob in cursor.fetchall():
        config = json.loads(blob)
        check_nested_models(config, f"Team {team_id}", "")
    
    conn.close()

def check_nested_models(obj, team_id, path):
    """Recursively check for models in nested structures"""
    if isinstance(obj, dict):
        if 'config' in obj and isinstance(obj['config'], dict):
            cfg = obj['config']
            if 'model' in cfg:
                model_name = cfg.get('model')
                model_info = cfg.get('model_info')
                print(f"\n{team_id} {path}")
                print(f"  Model: {model_name}")
                print(f"  Has model_info: {model_info is not None}")
                if model_info is None:
                    print(f"  ⚠️ MISSING model_info!")
        
        for key, value in obj.items():
            check_nested_models(value, team_id, f"{path}.{key}")
    
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            check_nested_models(item, team_id, f"{path}[{i}]")

if __name__ == "__main__":
    check_model_info()
