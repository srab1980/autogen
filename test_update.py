import sqlite3

DB_URI = "autogen04202.db"

def test_update():
    conn = sqlite3.connect(DB_URI)
    cursor = conn.cursor()
    
    print("Attempting to update gallery with quoted 'config' column...")
    try:
        # Just update ID 2 (which I saw in API response)
        # Note: API response said ID 2.
        # Check if ID 2 exists first
        cursor.execute("SELECT id FROM gallery WHERE id = 2")
        if not cursor.fetchone():
            print("ID 2 not found, finding any ID...")
            cursor.execute("SELECT id FROM gallery LIMIT 1")
            row = cursor.fetchone()
            if not row:
                print("No rows in gallery!")
                return
            target_id = row[0]
        else:
            target_id = 2
            
        print(f"Targeting ID {target_id}")
        
        # Read current config to be safe
        cursor.execute("SELECT config FROM gallery WHERE id = ?", (target_id,))
        current_config = cursor.fetchone()[0]
        
        # Update with same content
        cursor.execute('UPDATE gallery SET "config" = ? WHERE "id" = ?', (current_config, target_id))
        print("Update SUCCESS!")
        conn.commit()
        
    except Exception as e:
        print(f"Update FAILED: {e}")
        
    conn.close()

if __name__ == "__main__":
    test_update()
