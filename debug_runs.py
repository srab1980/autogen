"""
Debug: Check what's in the run table for Rafeeq team
"""
import sqlite3
import json

conn = sqlite3.connect('autogen04202.db')
cursor = conn.cursor()

# Check recent runs
print("=== RECENT RUNS ===")
cursor.execute("""
    SELECT r.id, r.session_id, s.team_id, r.messages, r.created_at
    FROM run r
    JOIN session s ON r.session_id = s.id
    ORDER BY r.created_at DESC
    LIMIT 5
""")

for row in cursor.fetchall():
    run_id, session_id, team_id, messages_blob, created_at = row
    messages = json.loads(messages_blob) if messages_blob else []
    print(f"\nRun {run_id}: Team {team_id}, Session {session_id}")
    print(f"  Created: {created_at}")
    print(f"  Messages count: {len(messages)}")
    if messages:
        print(f"  First message preview: {str(messages[0])[:200]}...")

# Also check message table if it exists
print("\n=== CHECKING FOR MESSAGE TABLE ===")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [r[0] for r in cursor.fetchall()]
print(f"Tables: {tables}")

if 'message' in tables:
    cursor.execute("SELECT COUNT(*) FROM message")
    print(f"Messages in message table: {cursor.fetchone()[0]}")
    cursor.execute("SELECT * FROM message LIMIT 1")
    print(f"Sample: {cursor.fetchone()}")

conn.close()
