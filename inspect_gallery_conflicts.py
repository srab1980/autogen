import sqlite3
import json

conn = sqlite3.connect('autogen04202.db')
c = conn.cursor()
c.execute('PRAGMA table_info(gallery)')
cols = c.fetchall()
col_names = [col[1] for col in cols]
print(f"Gallery columns: {col_names}")

# 'config' is the likely column
target_col = None
for name in ['config', 'component', 'data']:
    if name in col_names:
        target_col = name
        break

if target_col:
    print(f"Scanning column: {target_col}")
    c.execute(f"SELECT id, {target_col} FROM gallery")
    rows = c.fetchall()
    print(f"Found {len(rows)} galleries.")
    
    for row in rows:
        gid = row[0]
        data_str = row[1]
        if not data_str: continue
        try:
            data = json.loads(data_str)
            
            # Helper to check recursive like before
            def check_recursive(obj, path, context):
                if isinstance(obj, dict):
                    has_wb = "workbench" in obj
                    has_tools = "tools" in obj and obj["tools"] is not None and len(obj["tools"]) > 0
                    if has_wb and has_tools:
                        print(f"CONFLICT in {context} at {path}")
                    
                    for k, v in obj.items():
                        check_recursive(v, f"{path}.{k}", context)
                elif isinstance(obj, list):
                    for i, item in enumerate(obj):
                        check_recursive(item, f"{path}[{i}]", context)

            check_recursive(data, "root", f"Gallery {gid}")

        except Exception as e:
            print(f"Error parsing gallery {gid}: {e}")
else:
    print("Could not find config/component/data column in gallery")
conn.close()
