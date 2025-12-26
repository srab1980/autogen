import sqlite3
import sys
import os

def inspect_db(db_path):
    if not os.path.exists(db_path):
        print(f"Error: {db_path} not found")
        return

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print(f"Database: {db_path}")
        print(f"Tables found: {len(tables)}")
        
        for table in tables:
            table_name = table[0]
            print(f"- {table_name}")
            try:
                cursor.execute(f"SELECT count(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                print(f"  Rows: {count}")
            except Exception as e:
                print(f"  Error counting rows: {e}")

        conn.close()

    except Exception as e:
        print(f"Error reading {db_path}: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        inspect_db(sys.argv[1])
    else:
        print("Usage: python inspect_db.py <db_path>")
