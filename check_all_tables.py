"""
Check ALL tables for 'para' in source code
"""
import sqlite3
import json
import re

DB_PATH = "autogen04202.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print("=== CHECKING ALL TABLES FOR 'def...para' ===\n")

# Check Gallery
cursor.execute("SELECT id, config FROM gallery")
for row in cursor.fetchall():
    row_id, config_blob = row
    if config_blob and 'def ' in config_blob and 'para' in config_blob:
        # Check for function with para parameter  
        matches = re.findall(r'def\s+\w+\s*\([^)]*para[^)]*\)', config_blob)
        if matches:
            print(f"Gallery {row_id}: {matches}")

# Check Team
cursor.execute("SELECT id, component FROM team")
for row in cursor.fetchall():
    team_id, config_blob = row
    if config_blob and 'def ' in config_blob and 'para' in config_blob:
        matches = re.findall(r'def\s+\w+\s*\([^)]*para[^)]*\)', config_blob)
        if matches:
            print(f"Team {team_id}: {matches}")

# Check if there are other teams being used
cursor.execute("SELECT id, team_id FROM session ORDER BY created_at DESC LIMIT 5")
print("\nRecent sessions:")
for row in cursor.fetchall():
    print(f"  Session {row[0]}: Team {row[1]}")

conn.close()
print("\n✅ Done checking!")
