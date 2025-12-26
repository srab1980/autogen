"""
Remove calculator tools from agents that don't need them
"""
import sqlite3
import json

DB_PATH = "autogen04202.db"

def remove_calculator_tools(config_obj, path=""):
    """Remove calculator tools from workbenches"""
    changed = False
    
    if isinstance(config_obj, dict):
        # Check if this is a workbench with tools
        if 'tools' in config_obj and isinstance(config_obj['tools'], list):
            original_count = len(config_obj['tools'])
            # Keep only export tools, remove calculators
            config_obj['tools'] = [
                tool for tool in config_obj['tools']
                if tool.get('config', {}).get('name', '') != 'calculator'
            ]
            if len(config_obj['tools']) < original_count:
                removed = original_count - len(config_obj['tools'])
                print(f"  Removed {removed} calculator tool(s) from {path}")
                changed = True
        
        for key, value in config_obj.items():
            if remove_calculator_tools(value, f"{path}.{key}"):
                changed = True
    
    elif isinstance(config_obj, list):
        for i, item in enumerate(config_obj):
            if remove_calculator_tools(item, f"{path}[{i}]"):
                changed = True
    
    return changed

def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("=== REMOVING CALCULATOR TOOLS ===")
    
    # Fix Rafeeq2 team
    cursor.execute("SELECT id, component FROM team WHERE id = 4")
    row = cursor.fetchone()
    if row:
        config = json.loads(row[1])
        if remove_calculator_tools(config, "rafeeq2"):
            cursor.execute("UPDATE team SET component = ? WHERE id = ?", 
                         (json.dumps(config), 4))
            print("\n✓ Rafeeq2 UPDATED")
    
    conn.commit()
    conn.close()
    print("\n✅ Calculator tools removed!")

if __name__ == "__main__":
    main()
