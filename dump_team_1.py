import sqlite3
import json

def dump():
    conn = sqlite3.connect('autogen04202.db')
    cursor = conn.cursor()
    cursor.execute('SELECT component FROM team WHERE id=1')
    row = cursor.fetchone()
    if row:
        data = json.loads(row[0])
        with open('team_1_dump.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print("Dumped team 1 to team_1_dump.json")
    else:
        print("Team 1 not found")
    conn.close()

if __name__ == "__main__":
    dump()
