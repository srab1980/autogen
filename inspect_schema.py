import sqlite3
import sys
import os

def inspect_schema(db_path):
    if not os.path.exists(db_path):
        print(f"Error: {db_path} not found")
        return

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print(f"Database: {db_path}")
        
        for table in tables:
            table_name = table[0]
            print(f"\nTable: {table_name}")
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            for col in columns:
                # col structure: (cid, name, type, notnull, dflt_value, pk)
                print(f"  - {col[1]} ({col[2]})")

        conn.close()

    except Exception as e:
        print(f"Error reading {db_path}: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        inspect_schema(sys.argv[1])
    else:
        print("Usage: python inspect_schema.py <db_path>")
