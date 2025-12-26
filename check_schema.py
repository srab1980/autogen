import sqlite3
import os

DB_URI = "autogen04202.db"

if not os.path.exists(DB_URI):
    print("DB not found")
else:
    conn = sqlite3.connect(DB_URI)
    cursor = conn.cursor()
    
    print("--- Team Table ---")
    cursor.execute("PRAGMA table_info(team)")
    for row in cursor.fetchall():
        print(row)
        
    print("\n--- Gallery Table ---")
    cursor.execute("PRAGMA table_info(gallery)")
    for row in cursor.fetchall():
        print(row)
        
    conn.close()
