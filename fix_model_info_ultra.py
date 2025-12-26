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

# Known valid OpenAI models that don't need model_info
VALID_OPENAI_MODELS = {
    'gpt-4', 'gpt-4-turbo', 'gpt-4o', 'gpt-4o-mini',
    'gpt-3.5-turbo', 'gpt-3.5-turbo-16k',
    'text-embedding-ada-002', 'text-embedding-3-small', 'text-embedding-3-large'
}

def fix_model_info_aggressive(obj, path="root"):
    """Aggressively add model_info to ANY model configuration found"""
    modified = False
    
    if isinstance(obj, dict):
        # Check if this dict has BOTH 'model' and 'api_key' - likely a model config
        if 'model' in obj and 'api_key' in obj:
            model_name = obj.get('model')
            print(f"  Found model config at {path}: {model_name}")
            
            # Check if it needs model_info
            if model_name not in VALID_OPENAI_MODELS:
                if 'model_info' not in obj or obj.get('model_info') is None:
                    print(f"    → Adding model_info to {model_name}")
                    obj['model_info'] = DEFAULT_MODEL_INFO.copy()
                    modified = True
                else:
                    print(f"    ✓ Already has model_info")
        
        # Also check for 'config' blocks that might contain models
        if 'config' in obj and isinstance(obj['config'], dict):
            cfg = obj['config']
            if 'model' in cfg:
                model_name = cfg.get('model')
                print(f"  Found model in config at {path}: {model_name}")
                
                if model_name not in VALID_OPENAI_MODELS:
                    if 'model_info' not in cfg or cfg.get('model_info') is None:
                        print(f"    → Adding model_info to {model_name}")
                        cfg['model_info'] = DEFAULT_MODEL_INFO.copy()
                        modified = True
                    else:
                        print(f"    ✓ Already has model_info")
        
        # Recurse into ALL dict values
        for key, value in obj.items():
            if fix_model_info_aggressive(value, f"{path}.{key}"):
                modified = True
    
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            if fix_model_info_aggressive(item, f"{path}[{i}]"):
                modified = True
    
    return modified

def main():
    if not os.path.exists(DB_PATH):
        print(f"Database {DB_PATH} not found.")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Fix Gallery
    print("=== FIXING GALLERY (AGGRESSIVE) ===")
    cursor.execute("SELECT id, config FROM gallery")
    for row_id, blob in cursor.fetchall():
        config = json.loads(blob)
        print(f"\nGallery ID {row_id}: {config.get('label', 'UNKNOWN')}")
        
        if fix_model_info_aggressive(config, f"gallery.{row_id}"):
            cursor.execute("UPDATE gallery SET config = ? WHERE id = ?", 
                         (json.dumps(config), row_id))
            print(f"  ✓ UPDATED")
    
    # Fix Teams
    print("\n=== FIXING TEAMS (AGGRESSIVE) ===")
    cursor.execute("SELECT id, component FROM team")
    team_rows = cursor.fetchall()
    for team_id, blob in team_rows:
        config = json.loads(blob)
        print(f"\nTeam ID {team_id}")
        
        if fix_model_info_aggressive(config, f"team.{team_id}"):
            cursor.execute("UPDATE team SET component = ? WHERE id = ?", 
                         (json.dumps(config), team_id))
            print(f"  ✓ UPDATED")
    
    conn.commit()
    conn.close()
    
    print("\n✅ Aggressive fix complete!")

if __name__ == "__main__":
    main()
