
import sqlite3
import json

def fix_agent_versions():
    db_path = 'autogen04202.db'
    conn = sqlite3.connect(db_path)
    # Use dict factory to access columns by name
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    print(f"Connected to {db_path}")

    # 1. Update 'gallery' table
    try:
        cursor.execute("SELECT id, config, version, component_type FROM gallery")
        rows = cursor.fetchall()
        for row in rows:
            try:
                config = json.loads(row['config'])
                # Check if it is an AssistantAgent
                # In gallery, provider is usually in the config or top level? 
                # The dump shows 'provider' is actually part of the component structure, but here we just have 'config' column which is the inner config?
                # Wait, looking at dump:
                # ID: 1, ... config: { "provider": "...", "config": {...} } ? 
                # No, the dump shows the *row* has keys "provider", "component_type".
                # But querying 'gallery', we usually just see 'config' blob.
                # Let's check the dump format again.
                # The dump script did: cursor.execute("SELECT * FROM gallery")
                # And the output for ID 1 (Teams) shows:
                # { "provider": "...", "config": { ... } }
                # The 'config' column in DB likely stores the whole JSON structure shown in the dump.
                
                # Let's trust the 'provider' key in the parsed json.
                if config.get('provider') == 'autogen_agentchat.agents.AssistantAgent':
                    if row['version'] == 1:
                        # Check if it has 'model_client' in the inner config
                        inner_config = config.get('config', {})
                        if 'model_client' in inner_config:
                            print(f"Upgrading Gallery Agent ID {row['id']} from v1 to v2")
                            
                            # update version in top level columns
                            # Also update 'version' and 'component_version' inside the JSON
                            config['version'] = 2
                            config['component_version'] = 2
                            
                            new_config_json = json.dumps(config)
                            
                            cursor.execute(
                                "UPDATE gallery SET version = 2, config = ? WHERE id = ?",
                                (new_config_json, row['id'])
                            )
            except json.JSONDecodeError:
                pass
    except Exception as e:
        print(f"Error processing gallery: {e}")

    # 2. Update 'team' table
    # Teams have a 'component' column which is the JSON blob
    try:
        cursor.execute("SELECT id, component FROM team")
        rows = cursor.fetchall()
        for row in rows:
            try:
                component = json.loads(row['component'])
                
                # Recursive function to find and update AssistantAgents
                updated = False
                
                def upgrade_node(node):
                    nonlocal updated
                    if isinstance(node, dict):
                        # Check if this node is an AssistantAgent
                        if node.get('provider') == 'autogen_agentchat.agents.AssistantAgent':
                             if node.get('version') == 1:
                                 inner_conf = node.get('config', {})
                                 if 'model_client' in inner_conf:
                                     print(f"  Found nested AssistantAgent v1 -> v2")
                                     node['version'] = 2
                                     node['component_version'] = 2
                                     updated = True
                        
                        # Recurse into values
                        for key, value in node.items():
                            if isinstance(value, (dict, list)):
                                upgrade_node(value)
                    elif isinstance(node, list):
                        for item in node:
                            upgrade_node(item)

                upgrade_node(component)
                
                if updated:
                    print(f"Upgrading Team ID {row['id']}")
                    new_component_json = json.dumps(component)
                    cursor.execute(
                        "UPDATE team SET component = ? WHERE id = ?",
                        (new_component_json, row['id'])
                    )

            except json.JSONDecodeError:
                pass
    except Exception as e:
        print(f"Error processing team: {e}")

    conn.commit()
    conn.close()
    print("Database update complete.")

if __name__ == "__main__":
    fix_agent_versions()
