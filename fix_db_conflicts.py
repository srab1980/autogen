import sqlite3
import json

db_path = 'autogen04202.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

def fix_recursive(obj, path, modified_flag):
    if isinstance(obj, dict):
        has_workbench = "workbench" in obj
        has_tools = "tools" in obj and obj["tools"] is not None and len(obj["tools"]) > 0
        
        if has_workbench and has_tools:
             print(f"Fixing conflict at {path}...")
             # Remove 'tools' key
             del obj["tools"]
             return True
             
        for k, v in obj.items():
            if fix_recursive(v, f"{path}.{k}", False):
                modified_flag = True
                
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            if fix_recursive(item, f"{path}[{i}]", False):
                modified_flag = True
                
    return modified_flag

cursor.execute("SELECT id, component FROM team WHERE id=4") # Targeting specific ID first
row = cursor.fetchone()
if row:
    team_id = row[0]
    comp_json = json.loads(row[1])
    
    if fix_recursive(comp_json, "root", False):
        print(f"Updating Team {team_id}...")
        new_comp_str = json.dumps(comp_json, ensure_ascii=False) # Keep arabic safe if any
        cursor.execute("UPDATE team SET component=? WHERE id=?", (new_comp_str, team_id))
        conn.commit()
    else:
        print("No changes needed.")

conn.close()
