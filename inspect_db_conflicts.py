import sqlite3
import json

db_path = 'autogen04202.db'
print(f"Connecting to {db_path}...")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [t[0] for t in cursor.fetchall()]
print("Tables:", tables)

tables_with_component = []
for t in tables:
    cursor.execute(f"PRAGMA table_info({t})")
    cols = [c[1] for c in cursor.fetchall()]
    if 'component' in cols:
        tables_with_component.append(t)

print("Tables with 'component' column:", tables_with_component)

log_file = open("conflict_report.txt", "w", encoding="utf-8")

def log(msg):
    print(msg)
    log_file.write(msg + "\n")

def check_recursive(obj, path, context_info):
    if isinstance(obj, dict):
        has_workbench = "workbench" in obj
        has_tools = "tools" in obj and obj["tools"] is not None and len(obj["tools"]) > 0
        
        if has_workbench and has_tools:
                log(f"!!! CONFLICT FOUND !!!")
                log(f"Context: {context_info}")
                log(f"Path: {path}")
                log("Object has both 'workbench' and 'tools' populated.")
                
        for k, v in obj.items():
            check_recursive(v, f"{path}.{k}", context_info)
            
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            check_recursive(item, f"{path}[{i}]", context_info)

for t in tables_with_component:
    try:
        cursor.execute(f"SELECT id, component FROM {t}")
        rows = cursor.fetchall()
        print(f"Scanning {len(rows)} rows in {t}...")
        for row in rows:
            row_id = row[0]
            comp_str = row[1]
            if not comp_str: continue
            try:
                comp_json = json.loads(comp_str)
                label = comp_json.get("label", "Unknown")
                check_recursive(comp_json, "root", f"Table: {t}, ID: {row_id}, Label: {label}")
            except json.JSONDecodeError:
                print(f"Error decoding JSON in {t} id={row_id}")
    except Exception as e:
        print(f"Error scanning {t}: {e}")

conn.close()
log_file.close()
