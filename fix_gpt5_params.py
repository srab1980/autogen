"""
Remove max_tokens from gpt-5.x model configurations
GPT-5.1 and GPT-5.2 don't support max_tokens parameter
"""
import sqlite3
import json

DB_PATH = "autogen04202.db"

def remove_max_tokens(obj, path="root"):
    """Remove max_tokens from gpt-5.x model configs"""
    modified = False
    
    if isinstance(obj, dict):
        # Check if this is a gpt-5.x model config
        if 'config' in obj and isinstance(obj['config'], dict):
            cfg = obj['config']
            model = cfg.get('model', '')
            
            if 'gpt-5' in model.lower():
                if 'max_tokens' in cfg:
                    print(f"  {path}: Removing max_tokens from {model}")
                    del cfg['max_tokens']
                    modified = True
        
        # Also check direct model configs (without nested 'config')
        if 'model' in obj and 'api_key' in obj:
            model = obj.get('model', '')
            if 'gpt-5' in model.lower():
                if 'max_tokens' in obj:
                    print(f"  {path}: Removing max_tokens from {model}")
                    del obj['max_tokens']
                    modified = True
        
        # Recurse
        for key, value in obj.items():
            if remove_max_tokens(value, f"{path}.{key}"):
                modified = True
    
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            if remove_max_tokens(item, f"{path}[{i}]"):
                modified = True
    
    return modified

def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Fix Gallery
    print("=== REMOVING max_tokens FROM GALLERY ===")
    cursor.execute("SELECT id, config FROM gallery")
    for row_id, blob in cursor.fetchall():
        config = json.loads(blob)
        if remove_max_tokens(config):
            cursor.execute("UPDATE gallery SET config = ? WHERE id = ?", 
                         (json.dumps(config), row_id))
            print(f"  Gallery {row_id} ✓ UPDATED")
    
    # Fix Teams
    print("\n=== REMOVING max_tokens FROM TEAMS ===")
    cursor.execute("SELECT id, component FROM team")
    for team_id, blob in cursor.fetchall():
        config = json.loads(blob)
        if remove_max_tokens(config):
            cursor.execute("UPDATE team SET component = ? WHERE id = ?", 
                         (json.dumps(config), team_id))
            print(f"  Team {team_id} ✓ UPDATED")
    
    conn.commit()
    conn.close()
    print("\n✅ max_tokens removed from all gpt-5.x models!")

if __name__ == "__main__":
    main()
