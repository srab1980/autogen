
"""
Remove 'stop' and 'max_tokens' parameters from gpt-5.x/o1 model configurations
These models don't support these parameters and cause BadRequestError
"""
import sqlite3
import json

DB_PATH = "autogen04202.db"

def fix_model_config(obj, path="root"):
    """Remove stop and max_tokens from model configs"""
    modified = False
    
    if isinstance(obj, dict):
        # Check if this is a model config
        if 'config' in obj and isinstance(obj['config'], dict):
            cfg = obj['config']
            model = cfg.get('model', '')
            
            # Target GPT-5 and o1 models
            if any(x in model.lower() for x in ['gpt-5', 'o1-', 'preview']):
                # Remove max_tokens
                if 'max_tokens' in cfg and cfg['max_tokens'] is not None:
                    print(f"  {path}: Removing max_tokens from {model}")
                    del cfg['max_tokens']
                    modified = True
                
                # Remove stop
                if 'stop' in cfg:
                    print(f"  {path}: Removing stop from {model}")
                    del cfg['stop']
                    modified = True
                    
        # Also check direct model configs (without nested 'config')
        if 'model' in obj:
            model = obj.get('model', '')
            if any(x in model.lower() for x in ['gpt-5', 'o1-', 'preview']):
                 # Remove max_tokens
                if 'max_tokens' in obj and obj['max_tokens'] is not None:
                    print(f"  {path}: Removing max_tokens from {model}")
                    del obj['max_tokens']
                    modified = True
                
                # Remove stop
                if 'stop' in obj:
                    print(f"  {path}: Removing stop from {model}")
                    del obj['stop']
                    modified = True

        # Recurse
        for key, value in obj.items():
            if fix_model_config(value, f"{path}.{key}"):
                modified = True
    
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            if fix_model_config(item, f"{path}[{i}]"):
                modified = True
    
    return modified

def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Fix Gallery
    print("=== FIXING MODEL PARAMS IN GALLERY ===")
    cursor.execute("SELECT id, config FROM gallery")
    for row_id, blob in cursor.fetchall():
        if not blob: continue
        try:
            config = json.loads(blob)
            if fix_model_config(config):
                cursor.execute("UPDATE gallery SET config = ? WHERE id = ?", 
                             (json.dumps(config), row_id))
                print(f"  Gallery {row_id} ✓ UPDATED")
        except json.JSONDecodeError:
            print(f"  Gallery {row_id} - Invalid JSON")
    
    # Fix Teams
    print("\n=== FIXING MODEL PARAMS IN TEAMS ===")
    cursor.execute("SELECT id, component FROM team")
    for team_id, blob in cursor.fetchall():
        if not blob: continue
        try:
            config = json.loads(blob)
            if fix_model_config(config):
                cursor.execute("UPDATE team SET component = ? WHERE id = ?", 
                             (json.dumps(config), team_id))
                print(f"  Team {team_id} ✓ UPDATED")
        except json.JSONDecodeError:
            print(f"  Team {team_id} - Invalid JSON")
    
    conn.commit()
    conn.close()
    print("\n✅ Cleanup complete!")

if __name__ == "__main__":
    main()
