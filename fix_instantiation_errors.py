import sqlite3
import json

DB_PATH = 'autogen04202.db'

DEFAULT_MODEL_INFO = {
    "vision": True,
    "function_calling": True,
    "json_output": True,
    "family": "gpt-5",
    "structured_output": True,
    "multiple_system_messages": True
}

def upgrade_node(node):
    updated = False
    if isinstance(node, dict):
        # 1. Handle Model Client
        if 'model_client' in node:
            mc = node['model_client']
            if isinstance(mc, dict) and 'config' in mc:
                model_info = mc['config'].get('model_info')
                if not model_info or model_info == "NOT SET":
                    print(f"  Fixing model_info for model: {mc['config'].get('model')}")
                    mc['config']['model_info'] = DEFAULT_MODEL_INFO
                    updated = True

        # 2. Handle Versioning for AssistantAgent
        if node.get('provider') == 'autogen_agentchat.agents.AssistantAgent':
            if node.get('version') != 2:
                print(f"  Upgrading AssistantAgent '{node.get('label')}' to v2")
                node['version'] = 2
                node['component_version'] = 2
                updated = True
        
        # 3. Handle models directly in some structures
        if 'model' in node and 'model_info' not in node and isinstance(node.get('model'), str):
             # This might be a standalone model config
             pass

        # Recurse
        for key, value in node.items():
            if upgrade_node(value):
                updated = True
                
    elif isinstance(node, list):
        for item in node:
            if upgrade_node(item):
                updated = True
                
    return updated

def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Process Tables
    tables_to_fix = [
        ('team', 'component'),
        ('gallery', 'config'),
        ('settings', 'config'),
    ]

    for table, column in tables_to_fix:
        print(f"Processing table: {table}")
        cursor.execute(f"SELECT id, {column} FROM {table}")
        rows = cursor.fetchall()
        
        for row_id, blob in rows:
            if not blob:
                continue
            try:
                data = json.loads(blob)
                if upgrade_node(data):
                    print(f"  Updating {table} ID {row_id}")
                    cursor.execute(f"UPDATE {table} SET {column} = ? WHERE id = ?", (json.dumps(data), row_id))
            except Exception as e:
                print(f"  Error processing {table} ID {row_id}: {e}")

    conn.commit()
    conn.close()
    print("Database patching complete.")

if __name__ == "__main__":
    main()
