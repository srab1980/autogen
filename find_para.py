"""Find ALL instances of 'para' in the team config"""
import sqlite3
import json

conn = sqlite3.connect('autogen04202.db')
cursor = conn.cursor()

cursor.execute("SELECT component FROM team WHERE id = 4")
config_str = cursor.fetchone()[0]

# Search for 'para' in the raw JSON
if 'para' in config_str:
    print("Found 'para' in config! Locations:")
    
    # Find surrounding context
    import re
    matches = list(re.finditer(r'.{50}para.{50}', config_str))
    for i, m in enumerate(matches[:10]):  # Show first 10
        print(f"\n{i+1}. ...{m.group()}...")
else:
    print("No 'para' found in config!")

conn.close()
