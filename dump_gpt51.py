import sqlite3
import json

def dump():
    conn = sqlite3.connect('autogen04202.db')
    cursor = conn.cursor()
    results = {}
    
    for table, col in [('team', 'component'), ('gallery', 'config')]:
        cursor.execute(f"SELECT id, {col} FROM {table}")
        for row_id, blob in cursor.fetchall():
            if blob and 'gpt-5.1' in blob:
                results[f"{table}_{row_id}"] = json.loads(blob)
                
    with open('gpt51_full_dump.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print("Dumped to gpt51_full_dump.json")
    conn.close()

if __name__ == "__main__":
    dump()
