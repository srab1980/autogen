import json
import sqlite3
import uuid
import datetime
import os

DB_PATH = "autogen04202.db"
JSON_FILES = [
    "temp_gallery.json",
    "autogen/python/packages/autogen-studio/notebooks/team.json",
    "autogen/python/packages/autogen-studio/notebooks/travel_team.json"
]

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_tables(cursor):
    print("Initializing tables if missing...")
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS agent (
        id TEXT PRIMARY KEY,
        user_id TEXT,
        created_at TEXT,
        updated_at TEXT,
        config TEXT,
        type TEXT
    )
    ''')
    # Added 'type' column just in case, but standard schema might not have it.
    # Actually standard schema: id, user_id, created_at, updated_at, config (json)

def extract_agents(data, found_agents):
    if isinstance(data, dict):
        # Check if this dict IS an agent
        if data.get("component_type") == "agent":
            # It's an agent definition
            config = data.get("config", {})
            name = config.get("name") if isinstance(config, dict) else None
            # fallback if name is top level (some versions)
            if not name:
                name = data.get("name")
            
            if name:
                # Store the FULL data as the config
                found_agents.append({"name": name, "config": data})
            
        # Recursive search in all values
        for key, value in data.items():
            extract_agents(value, found_agents)
            
    elif isinstance(data, list):
        for item in data:
            extract_agents(item, found_agents)

def merge_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    init_tables(cursor)

    existing_agent_names = set()
    try:
        cursor.execute("SELECT config FROM agent")
        rows = cursor.fetchall()
        for row in rows:
            try:
                cfg = json.loads(row['config'])
                # Name might be in config.name or config.config.name depending on structure
                name = cfg.get("config", {}).get("name") or cfg.get("name")
                if name:
                    existing_agent_names.add(name)
            except:
                pass
    except Exception as e:
        print(f"Error reading existing agents: {e}")

    print(f"Existing agents in DB: {existing_agent_names}")

    total_added = 0
    for file_path in JSON_FILES:
        if not os.path.exists(file_path):
            print(f"Skipping {file_path} (not found)")
            continue
        
        print(f"Processing {file_path}...")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            found_agents = []
            extract_agents(data, found_agents)
            
            print(f"  Found {len(found_agents)} potential agents.")
            
            for agent in found_agents:
                name = agent["name"]
                if name in existing_agent_names:
                    print(f"  Skipping duplicate agent: {name}")
                else:
                    print(f"  Adding agent: {name}")
                    new_id = str(uuid.uuid4())
                    now = datetime.datetime.now().isoformat()
                    config_str = json.dumps(agent["config"])
                    user_id = "default"

                    try:
                        cursor.execute(
                            "INSERT INTO agent (id, user_id, created_at, updated_at, config) VALUES (?, ?, ?, ?, ?)",
                            (new_id, user_id, now, now, config_str)
                        )
                        existing_agent_names.add(name)
                        total_added += 1
                    except Exception as e:
                         print(f"  Error inserting agent {name}: {e}")

        except Exception as e:
            print(f"Error reading {file_path}: {e}")

    conn.commit()
    conn.close()
    print(f"Merge completed. Total new agents added: {total_added}")

if __name__ == "__main__":
    merge_data()
