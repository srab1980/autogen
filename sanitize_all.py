import sqlite3
import json

def sanitize_config(config):
    changed = False
    
    # helper to process an agent config
    def process_agent(agent_conf):
        c = False
        # Check if it has config dict
        if "config" in agent_conf and isinstance(agent_conf["config"], dict):
            inner_conf = agent_conf["config"]
            # Check for workbench
            if "workbench" in inner_conf and inner_conf["workbench"]:
                # If workbench is present, REMOVE tools if present
                if "tools" in inner_conf:
                    print(f"  Removing 'tools' key from agent {inner_conf.get('name', 'unnamed')}")
                    del inner_conf["tools"]
                    c = True
        return c

    # Traverse structure
    # Teams have participants
    if "config" in config and "participants" in config["config"]:
        for part in config["config"]["participants"]:
            if process_agent(part):
                changed = True
    
    # Generic Agent (top level)
    if process_agent(config):
        changed = True

    # Gallery structure
    if "components" in config and "agents" in config["components"]:
        for agent in config["components"]["agents"]:
            if process_agent(agent):
                changed = True
                
    return changed

def main():
    db_path = 'autogen04202.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Sanitize Teams
    cursor.execute("SELECT id, component FROM team")
    rows = cursor.fetchall()
    for row in rows:
        tid, config_str = row
        try:
            config = json.loads(config_str)
            if sanitize_config(config):
                print(f"Updating Team {tid}")
                cursor.execute("UPDATE team SET component=? WHERE id=?", (json.dumps(config), tid))
        except Exception as e:
            print(f"Error processing team {tid}: {e}")

    # Sanitize Gallery
    try:
        cursor.execute("SELECT id, config FROM gallery")
        rows = cursor.fetchall()
        for row in rows:
            gid, config_str = row
            if not config_str: continue
            try:
                config = json.loads(config_str)
                if sanitize_config(config):
                    print(f"Updating Gallery {gid}")
                    cursor.execute("UPDATE gallery SET config=? WHERE id=?", (json.dumps(config), gid))
            except Exception as e:
                print(f"Error processing gallery {gid}: {e}")
    except Exception as e:
        print(f"Error processing gallery table: {e}")

    conn.commit()
    conn.close()
    print("Sanitization complete.")

if __name__ == "__main__":
    main()
