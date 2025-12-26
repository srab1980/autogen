import sqlite3
import os
import json

HOME = os.path.expanduser("~")
DB_PATH = os.path.join(HOME, ".autogenstudio", "database.sqlite")

def main():
    print(f"Checking DB at: {DB_PATH}")
    if not os.path.exists(DB_PATH):
        print("DB file not found!")
        return

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        print("\n--- Gallery Table ---")
        cursor.execute("SELECT id, user_id, config FROM gallery")
        rows = cursor.fetchall()
        print(f"Row count: {len(rows)}")
        for row in rows:
            print(f"ID: {row[0]}, User: {row[1]}")
            config = json.loads(row[2])
            components = config.get("components", {})
            agents = components.get("agents", [])
            print(f"  Agent count in config: {len(agents)}")
            for a in agents:
                print(f"    - {a.get('label')}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    main()
