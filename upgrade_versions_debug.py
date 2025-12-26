import sqlite3
import json
import os
import traceback

DB_URI = "autogen04202.db"

def upgrade_component(comp):
    """
    Recursively upgrade component configurations.
    """
    if isinstance(comp, list):
        for item in comp:
            upgrade_component(item)
    elif isinstance(comp, dict):
        provider = comp.get("provider")
        
        # Match AssistantAgent
        # Also check for 'provider': 'autogen_agentchat.agents.AssistantAgent'
        if provider and "AssistantAgent" in provider:
             # Just to be safe, check generic "AssistantAgent" in string
             # because previous script used exact string match.
             pass

        if provider == "autogen_agentchat.agents.AssistantAgent":
            current_ver = comp.get("version")
            # Upgrade if not 2
            if current_ver != 2:
                print(f"  Upgrading AssistantAgent from version {current_ver} to 2")
                comp["version"] = 2
                comp["component_version"] = 2
            
            # Check workbench schema (must be list)
            config = comp.get("config", {})
            workbench = config.get("workbench")
            if workbench and isinstance(workbench, dict):
                print("  Fixing workbench schema (converting dict to list)")
                config["workbench"] = [workbench]
                comp["config"] = config # Ensure update
                
        # Recurse
        for key, value in comp.items():
            if isinstance(value, (dict, list)):
                 upgrade_component(value)

def main():
    if not os.path.exists(DB_URI):
        print(f"Database file {DB_URI} not found.")
        return

    conn = sqlite3.connect(DB_URI)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    print("Scanning Gallery...")
    try:
        cursor.execute("SELECT id, config FROM gallery")
        rows = cursor.fetchall()
        
        for row in rows:
            try:
                print(f"Processing Gallery ID {row['id']}")
                config = json.loads(row["config"])
                upgrade_component(config)
                
                new_config_str = json.dumps(config)
                if new_config_str != row["config"]:
                    cursor.execute("UPDATE gallery SET config = ? WHERE id = ?", (new_config_str, row["id"]))
                    print(f"  Updated Gallery ID {row['id']}")
            except Exception as e:
                print(f"  Error processing gallery {row['id']}: {e}")
                traceback.print_exc()

    except Exception as e:
        print(f"Global Error in Gallery loop: {e}")
        traceback.print_exc()

    print("\nScanning Teams...")
    try:
        cursor.execute("SELECT id, config FROM team")
        rows = cursor.fetchall()
        
        for row in rows:
            try:
                print(f"Processing Team ID {row['id']}")
                config = json.loads(row["config"])
                upgrade_component(config)
                
                new_config_str = json.dumps(config)
                if new_config_str != row["config"]:
                    cursor.execute("UPDATE team SET config = ? WHERE id = ?", (new_config_str, row["id"]))
                    print(f"  Updated Team ID {row['id']}")
            except Exception as e:
                print(f"  Error processing team {row['id']}: {e}")
                traceback.print_exc()

    except Exception as e:
         print(f"Global Error in Team loop: {e}")
         traceback.print_exc()

    conn.commit()
    conn.close()
    print("Done upgrading.")

if __name__ == "__main__":
    main()
