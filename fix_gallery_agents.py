
import sqlite3
import json

def fix_gallery_agents():
    db_path = 'autogen04202.db'
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    print(f"Fixing nested Gallery agents in {db_path}...")
    
    updates_made = False

    try:
        cursor.execute("SELECT id, config FROM gallery")
        rows = cursor.fetchall()
        for row in rows:
            try:
                gallery_updated = False
                config = json.loads(row['config'])
                
                # Check agents list
                if 'components' in config and 'agents' in config['components']:
                    agents = config['components']['agents']
                    for i, agent in enumerate(agents):
                        if agent.get('provider') == 'autogen_agentchat.agents.AssistantAgent':
                            if agent.get('version') == 1:
                                # Check if it looks like v2 (has model_client) or if we just force upgrade
                                # Assuming we want to force upgrade if it's the specific component triggering error
                                print(f"  Upgrading Agent '{agent.get('label')}' in Gallery {row['id']} from v1 to v2")
                                agent['version'] = 2
                                agent['component_version'] = 2
                                gallery_updated = True
                                updates_made = True
                
                if gallery_updated:
                    new_json = json.dumps(config)
                    cursor.execute("UPDATE gallery SET config = ? WHERE id = ?", (new_json, row['id']))

            except json.JSONDecodeError:
                pass
    except Exception as e:
        print(f"Error processing gallery: {e}")

    conn.commit()
    conn.close()
    
    if updates_made:
        print("Gallery agents updated successfully.")
    else:
        print("No stale agents found (or update failed).")

if __name__ == "__main__":
    fix_gallery_agents()
