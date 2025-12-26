"""
Fix gpt-5.1 and gpt-5.2 to use valid OpenAI model names
Keep the labels but change the actual API model name
"""
import sqlite3
import json
import os

DB_PATH = "autogen04202.db"

# Map custom model names to real OpenAI models
MODEL_MAPPING = {
    "gpt-5.1": "gpt-4o-mini",  # Use gpt-4o-mini as the backend
    "gpt-5.2": "gpt-4o-mini",  # Use gpt-4o-mini as the backend
    "OpenAI gpt-5.1": "gpt-4o-mini",
    "OpenAI gpt-5.2": "gpt-4o-mini"
}

def fix_model_names(obj, path="root"):
    """Recursively fix model names to use valid OpenAI models"""
    modified = False
    
    if isinstance(obj, dict):
        # Check for model in config
        if 'config' in obj and isinstance(obj['config'], dict):
            cfg = obj['config']
            if 'model' in cfg:
                current_model = cfg.get('model')
                if current_model in MODEL_MAPPING:
                    new_model = MODEL_MAPPING[current_model]
                    print(f"  {path}: Changing '{current_model}' -> '{new_model}'")
                    cfg['model'] = new_model
                    modified = True
        
        # Also check if 'model' is directly in this dict
        if 'model' in obj and 'api_key' in obj:
            current_model = obj.get('model')
            if current_model in MODEL_MAPPING:
                new_model = MODEL_MAPPING[current_model]
                print(f"  {path}: Changing '{current_model}' -> '{new_model}'")
                obj['model'] = new_model
                modified = True
        
        # Recurse
        for key, value in obj.items():
            if fix_model_names(value, f"{path}.{key}"):
                modified = True
    
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            if fix_model_names(item, f"{path}[{i}]"):
                modified = True
    
    return modified

def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Fix Gallery
    print("=== FIXING GALLERY ===")
    cursor.execute("SELECT id, config FROM gallery")
    for row_id, blob in cursor.fetchall():
        config = json.loads(blob)
        print(f"\nGallery ID {row_id}: {config.get('label')}")
        if fix_model_names(config, f"gallery.{row_id}"):
            cursor.execute("UPDATE gallery SET config = ? WHERE id = ?", 
                         (json.dumps(config), row_id))
            print(f"  ✓ UPDATED")
    
    # Fix Teams
    print("\n=== FIXING TEAMS ===")
    cursor.execute("SELECT id, component FROM team")
    for team_id, blob in cursor.fetchall():
        config = json.loads(blob)
        print(f"\nTeam ID {team_id}")
        if fix_model_names(config, f"team.{team_id}"):
            cursor.execute("UPDATE team SET component = ? WHERE id = ?", 
                         (json.dumps(config), team_id))
            print(f"  ✓ UPDATED")
    
    conn.commit()
    conn.close()
    print("\n✅ Model names fixed! All now use valid OpenAI API models.")

if __name__ == "__main__":
    main()
