import sqlite3
import json
import os
import traceback

DB_URI = "autogen04202.db"

def upgrade_component(comp):
    """
    Recursively upgrade component configurations.
    Returns True if modified.
    """
    modified = False
    
    if isinstance(comp, list):
        for item in comp:
            if upgrade_component(item):
                modified = True
    elif isinstance(comp, dict):
        provider = comp.get("provider")
        
        # Upgrade AssistantAgent
        if provider == "autogen_agentchat.agents.AssistantAgent":
            current_ver = comp.get("version")
            if current_ver != 2:
                print(f"  Upgrading AssistantAgent from version {current_ver} to 2")
                comp["version"] = 2
                comp["component_version"] = 2
                modified = True
            
            # Fix workbench
            config = comp.get("config", {})
            workbench = config.get("workbench")
            if workbench and isinstance(workbench, dict):
                print("  Fixing workbench schema (converting dict to list)")
                config["workbench"] = [workbench]
                comp["config"] = config
                modified = True
        
        # Recurse
        for key, value in comp.items():
            if isinstance(value, (dict, list)):
                if upgrade_component(value):
                    modified = True
                    
    return modified

def main():
    if not os.path.exists(DB_URI):
        print(f"Database file {DB_URI} not found.")
        return

    conn = sqlite3.connect(DB_URI)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # GALLERY
    print("Scanning Gallery...")
    try:
        cursor.execute("SELECT id, config FROM gallery")
        rows = cursor.fetchall()
        
        for row in rows:
            try:
                config = json.loads(row["config"])
                if upgrade_component(config):
                    new_config_str = json.dumps(config)
                    cursor.execute('UPDATE gallery SET "config" = ? WHERE "id" = ?', (new_config_str, row["id"]))
                    print(f"  Updated Gallery ID {row['id']}")
            except Exception as e:
                print(f"  Error processing gallery {row['id']}: {e}")
                traceback.print_exc()
    except Exception as e:
        print(f"Global Error in Gallery loop: {e}")

    # TEAMS
    print("\nScanning Teams...")
    try:
        cursor.execute("SELECT id, config FROM team")
        rows = cursor.fetchall()
        
        for row in rows:
            try:
                config = json.loads(row["config"])
                if upgrade_component(config):
                    new_config_str = json.dumps(config)
                    cursor.execute('UPDATE team SET "config" = ? WHERE "id" = ?', (new_config_str, row["id"]))
                    print(f"  Updated Team ID {row['id']}")
            except Exception as e:
                print(f"  Error processing team {row['id']}: {e}")
                traceback.print_exc()
    except Exception as e:
         print(f"Global Error in Team loop: {e}")

    conn.commit()
    conn.close()
    print("Done upgrading.")

if __name__ == "__main__":
    main()
