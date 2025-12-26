import sqlite3
import os

DB_URI = "autogen04202.db"

conn = sqlite3.connect(DB_URI)
cursor = conn.cursor()

print("STRICT SCHEMA CHECK FOR TEAM TABLE:")
cursor.execute("PRAGMA table_info(team)")
rows = cursor.fetchall()
for row in rows:
    # row is (cid, name, type, notnull, dflt_value, pk)
    print(f"Column: {row[1]}, Type: {row[2]}")

conn.close()
