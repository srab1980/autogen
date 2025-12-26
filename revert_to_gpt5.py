"""
Revert models back to gpt-5.1 and gpt-5.2 (real OpenAI models)
"""
import sqlite3
import json

DB_PATH = "autogen04202.db"

# Revert mapping - these ARE real OpenAI models
REVERT_MAPPING = {
    # In Gallery items labeled as 5.1 or 5.2, set the model correctly
}

def fix_to_real_models(obj, target_label, target_model, path="root"):
    """Set model to the correct gpt-5.x value based on label"""
    modified = False
    
    if isinstance(obj, dict):
        # Check if this matches our target label
        label = obj.get('label', '')
        if target_label.lower() in label.lower():
            # This is a model config for 5.1 or 5.2
            if 'config' in obj and isinstance(obj['config'], dict):
                cfg = obj['config']
                if 'model' in cfg and cfg['model'] != target_model:
                    print(f"  {path}: Setting model to '{target_model}' (was '{cfg['model']}')")
                    cfg['model'] = target_model
                    modified = True
        
        # Recurse
        for key, value in obj.items():
            if fix_to_real_models(value, target_label, target_model, f"{path}.{key}"):
                modified = True
    
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            if fix_to_real_models(item, target_label, target_model, f"{path}[{i}]"):
                modified = True
    
    return modified

def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Fix Gallery
    print("=== REVERTING GALLERY TO REAL GPT-5.x MODELS ===")
    cursor.execute("SELECT id, config FROM gallery")
    for row_id, blob in cursor.fetchall():
        config = json.loads(blob)
        label = config.get('label', '')
        print(f"\nGallery ID {row_id}: {label}")
        
        modified = False
        if '5.1' in label:
            if fix_to_real_models(config, '5.1', 'gpt-5.1'):
                modified = True
        if '5.2' in label:
            if fix_to_real_models(config, '5.2', 'gpt-5.2'):
                modified = True
        
        if modified:
            cursor.execute("UPDATE gallery SET config = ? WHERE id = ?", 
                         (json.dumps(config), row_id))
            print(f"  ✓ UPDATED")
    
    # Fix Teams - need to find model_client blocks and update based on label
    print("\n=== REVERTING TEAMS TO REAL GPT-5.x MODELS ===")
    cursor.execute("SELECT id, component FROM team")
    for team_id, blob in cursor.fetchall():
        config = json.loads(blob)
        print(f"\nTeam ID {team_id}")
        
        modified = False
        if fix_to_real_models(config, '5.1', 'gpt-5.1'):
            modified = True
        if fix_to_real_models(config, '5.2', 'gpt-5.2'):
            modified = True
        
        if modified:
            cursor.execute("UPDATE team SET component = ? WHERE id = ?", 
                         (json.dumps(config), team_id))
            print(f"  ✓ UPDATED")
    
    conn.commit()
    conn.close()
    print("\n✅ Models reverted to real gpt-5.1 and gpt-5.2!")

if __name__ == "__main__":
    main()
