"""
Find and show ALL locations with 'para' or 'export' in the config
"""
import sqlite3
import json
import re

DB_PATH = "autogen04202.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("SELECT component FROM team WHERE id = 4")
config_str = cursor.fetchone()[0]

print("=== SEARCHING FOR 'para' IN CONFIG ===\n")

# Find all occurrences of 'para' (not 'paragraph')
pattern = r'.{30}[^a-z]para[^g].{30}'
matches = re.findall(pattern, config_str, re.IGNORECASE)

for i, match in enumerate(matches[:20]):
    print(f"{i+1}. ...{match}...")

print(f"\n\nTotal 'para' occurrences (not paragraph): {len(matches)}")

# Also check for set_rtl
if 'set_rtl' in config_str:
    print("\n⚠️ Found 'set_rtl' function in config!")
    
# Check for def.*para
pattern2 = r'def\s+\w+\s*\([^)]*para[^)]*\)'
matches2 = re.findall(pattern2, config_str)
print(f"\nFunctions with 'para' parameter: {matches2}")

conn.close()
