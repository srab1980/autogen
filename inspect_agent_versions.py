
import sqlite3
import json
import os

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def inspect_table(cursor, table_name, file_handle):
    file_handle.write(f"\n--- Inspecting {table_name} ---\n")
    try:
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        for row in rows:
            # Try to identify if it's an agent
            data = None
            if 'config' in row: # gallery style
                try:
                    config = json.loads(row['config'])
                    if row.get('component_type') == 'agent':
                        file_handle.write(f"ID: {row.get('id')}, Version: {row.get('version')}\n")
                        file_handle.write(json.dumps(config, indent=2) + "\n")
                        file_handle.write("-" * 20 + "\n")
                except:
                    pass
            elif 'component' in row: # team style
                 try:
                    component = json.loads(row['component'])
                    # Team components might contain agents or be an agent itself
                    file_handle.write(f"ID: {row.get('id')}\n")
                    file_handle.write(json.dumps(component, indent=2) + "\n")
                    file_handle.write("-" * 20 + "\n")
                 except:
                    pass

    except sqlite3.OperationalError as e:
        file_handle.write(f"Error reading {table_name}: {e}\n")

def main():
    conn = sqlite3.connect('autogen04202.db')
    conn.row_factory = dict_factory
    cursor = conn.cursor()

    with open('agent_versions.txt', 'w', encoding='utf-8') as f:
        inspect_table(cursor, 'gallery', f)
        inspect_table(cursor, 'team', f)

    conn.close()

if __name__ == "__main__":
    main()
