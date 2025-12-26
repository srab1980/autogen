import sqlite3
import json
import os

DB_URI = "autogen04202.db"

def upgrade_component(comp):
    """
    Recursively upgrade component configurations.
    """
    if isinstance(comp, list):
        for item in comp:
            upgrade_component(item)
    elif isinstance(comp, dict):
        # check if this is an AssistantAgent config
        provider = comp.get("provider")
        
        if provider == "autogen_agentchat.agents.AssistantAgent":
            current_ver = comp.get("version")
            if current_ver != 2:
                print(f"Upgrading AssistantAgent from version {current_ver} to 2")
                comp["version"] = 2
                comp["component_version"] = 2
            
            # Check workbench schema (must be list)
            config = comp.get("config", {})
            workbench = config.get("workbench")
            if workbench and isinstance(workbench, dict):
                print("Fixing workbench schema (converting dict to list)")
                config["workbench"] = [workbench]
                comp["config"] = config # valid? yes reference.
                
        # Recurse into config, participants, teams, agents, etc.
        # Just valid keys that might contain more components
        for key, value in comp.items():
            if key in ["config", "components", "agents", "teams", "models", "tools", "terminations", "workbenches", "participants", "members"]:
                upgrade_component(value)
            elif isinstance(value, (dict, list)):
                 # Generic recursion for deep structures
                 upgrade_component(value)

def main():
    if not os.path.exists(DB_URI):
        print(f"Database file {DB_URI} not found.")
        return

    conn = sqlite3.connect(DB_URI)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # 1. Update Gallery
    print("Scanning Gallery...")
    cursor.execute("SELECT id, config FROM gallery")
    rows = cursor.fetchall()
    
    for row in rows:
        try:
            config = json.loads(row["config"])
            upgrade_component(config)
            
            # Update DB
            new_config_str = json.dumps(config)
            if new_config_str != row["config"]:
                cursor.execute("UPDATE gallery SET config = ? WHERE id = ?", (new_config_str, row["id"]))
                print(f"Updated Gallery ID {row['id']}")
        except Exception as e:
            print(f"Error processing gallery {row['id']}: {e}")

    # 2. Update Teams
    print("Scanning Teams...")
    cursor.execute("SELECT id, config FROM team")
    rows = cursor.fetchall()
    
    for row in rows:
        try:
            config = json.loads(row["config"])
            upgrade_component(config)
            
            # Update DB
            new_config_str = json.dumps(config)
            if new_config_str != row["config"]:
                cursor.execute("UPDATE team SET config = ? WHERE id = ?", (new_config_str, row["id"]))
                print(f"Updated Team ID {row['id']}")
        except Exception as e:
             print(f"Error processing team {row['id']}: {e}")

    conn.commit()
    conn.close()
    print("Done upgrading.")

if __name__ == "__main__":
    main()
