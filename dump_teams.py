import sqlite3
import json
import os

DB_PATH = "autogen04202.db"

def dump_team_config(team_id):
    """Dump the configuration of a specific team"""
    if not os.path.exists(DB_PATH):
        print(f"Database {DB_PATH} not found.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, component FROM team WHERE id = ?", (team_id,))
    row = cursor.fetchone()
    
    if row:
        config = json.loads(row[1])
        print(f"=== Team {team_id} Configuration ===")
        print(json.dumps(config, indent=2))
        
        # Save to file
        with open(f"team_{team_id}_config.json", "w") as f:
            json.dump(config, f, indent=2)
        print(f"\n✓ Saved to team_{team_id}_config.json")
    else:
        print(f"Team {team_id} not found")
    
    conn.close()

if __name__ == "__main__":
    # Dump all teams
    import sys
    if len(sys.argv) > 1:
        dump_team_config(int(sys.argv[1]))
    else:
        # Dump all teams
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM team")
        for row in cursor.fetchall():
            dump_team_config(row[0])
        conn.close()
