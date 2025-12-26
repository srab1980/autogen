import sqlite3
import json

DB_PATH = 'autogen04202.db'

def find():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    tables = [('team', 'component'), ('gallery', 'config')]
    for table, column in tables:
        print(f"Searching in {table}...")
        cursor.execute(f"SELECT id, {column} FROM {table}")
        for row_id, blob in cursor.fetchall():
            if blob and 'gpt-5.1' in blob:
                print(f"  Found gpt-5.1 in {table} ID {row_id}")
    conn.close()

if __name__ == "__main__":
    find()
