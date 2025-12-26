
import sqlite3
import json

def fix_workbench_list():
    db_path = 'autogen04202.db'
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    print(f"Connected to {db_path} to fix workbench list schema.")

    # Shared logic to update a config dict
    def update_config(config, name_hint="Unknown"):
        updated = False
        # inner config usually has 'workbench' key
        inner_config = config.get('config', {})
        
        if 'workbench' in inner_config:
            wb = inner_config['workbench']
            if isinstance(wb, dict):
                print(f"  Fixing workbench for agent '{name_hint}': dict -> list")
                inner_config['workbench'] = [wb]
                updated = True
        
        return updated, config

    # 1. Update 'gallery' table
    try:
        cursor.execute("SELECT id, config FROM gallery")
        rows = cursor.fetchall()
        for row in rows:
            try:
                config = json.loads(row['config'])
                if config.get('provider') == 'autogen_agentchat.agents.AssistantAgent':
                    is_updated, new_config = update_config(config, f"Gallery item {row['id']}")
                    if is_updated:
                        new_json = json.dumps(new_config)
                        cursor.execute("UPDATE gallery SET config = ? WHERE id = ?", (new_json, row['id']))
            except json.JSONDecodeError:
                pass
    except Exception as e:
        print(f"Error processing gallery: {e}")

    # 2. Update 'team' table (recursive)
    try:
        cursor.execute("SELECT id, component FROM team")
        rows = cursor.fetchall()
        for row in rows:
            try:
                component = json.loads(row['component'])
                team_updated = False

                def process_node(node):
                    nonlocal team_updated
                    if isinstance(node, dict):
                        # check if it's an AssistantAgent
                        if node.get('provider') == 'autogen_agentchat.agents.AssistantAgent':
                             is_updated, _ = update_config(node, "Nested Agent")
                             if is_updated:
                                 team_updated = True
                        
                        for key, value in node.items():
                            if isinstance(value, (dict, list)):
                                process_node(value)
                    elif isinstance(node, list):
                        for item in node:
                            process_node(item)

                process_node(component)

                if team_updated:
                    print(f"Updating Team ID {row['id']}")
                    new_json = json.dumps(component)
                    cursor.execute("UPDATE team SET component = ? WHERE id = ?", (new_json, row['id']))
            except json.JSONDecodeError:
                pass
    except Exception as e:
        print(f"Error processing team: {e}")

    conn.commit()
    conn.close()
    print("Workbench list fix complete.")

if __name__ == "__main__":
    fix_workbench_list()
