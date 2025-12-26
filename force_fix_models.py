"""
Force update ALL models to use correct gpt-5.x names based on labels
"""
import sqlite3
import json

DB_PATH = "autogen04202.db"

def force_fix_model(obj, path="root"):
    """Force fix model names based on the label"""
    modified = False
    
    if isinstance(obj, dict):
        label = obj.get('label', '')
        
        # Check if this is a model configuration
        if 'config' in obj and isinstance(obj['config'], dict):
            cfg = obj['config']
            
            # If label contains 5.1, force model to gpt-5.1
            if '5.1' in label and 'model' in cfg:
                if cfg['model'] != 'gpt-5.1':
                    print(f"  {path}: FORCING model from '{cfg['model']}' -> 'gpt-5.1' (label: {label})")
                    cfg['model'] = 'gpt-5.1'
                    modified = True
            
            # If label contains 5.2, force model to gpt-5.2
            if '5.2' in label and 'model' in cfg:
                if cfg['model'] != 'gpt-5.2':
                    print(f"  {path}: FORCING model from '{cfg['model']}' -> 'gpt-5.2' (label: {label})")
                    cfg['model'] = 'gpt-5.2'
                    modified = True
        
        # Recurse into all nested objects
        for key, value in obj.items():
            if force_fix_model(value, f"{path}.{key}"):
                modified = True
    
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            if force_fix_model(item, f"{path}[{i}]"):
                modified = True
    
    return modified

def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Fix ALL Gallery items
    print("=== FORCE FIXING ALL GALLERY ITEMS ===")
    cursor.execute("SELECT id, config FROM gallery")
    all_gallery = cursor.fetchall()
    
    for row_id, blob in all_gallery:
        config = json.loads(blob)
        print(f"\nGallery ID {row_id}: {config.get('label', 'NO LABEL')}")
        
        if force_fix_model(config):
            cursor.execute("UPDATE gallery SET config = ? WHERE id = ?", 
                         (json.dumps(config), row_id))
            print(f"  ✓ UPDATED")
        else:
            # Check current model value
            model = config.get('config', {}).get('model', 'N/A')
            print(f"  Current model: {model}")
    
    # Fix ALL Team items
    print("\n=== FORCE FIXING ALL TEAM ITEMS ===")
    cursor.execute("SELECT id, component FROM team")
    all_teams = cursor.fetchall()
    
    for team_id, blob in all_teams:
        config = json.loads(blob)
        print(f"\nTeam ID {team_id}: {config.get('label', 'NO LABEL')}")
        
        if force_fix_model(config):
            cursor.execute("UPDATE team SET component = ? WHERE id = ?", 
                         (json.dumps(config), team_id))
            print(f"  ✓ UPDATED")
    
    conn.commit()
    conn.close()
    
    print("\n" + "="*50)
    print("✅ ALL models force-updated!")
    print("Please restart the AutoGen Studio server to see changes in UI.")

if __name__ == "__main__":
    main()
