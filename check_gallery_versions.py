
import sqlite3
import json

def check_gallery_versions():
    db_path = 'autogen04202.db'
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    print(f"Checking Gallery versions in {db_path}...")

    try:
        cursor.execute("SELECT id, config FROM gallery")
        rows = cursor.fetchall()
        for row in rows:
            try:
                config = json.loads(row['config'])
                components = config.get('components', {})
                agents = components.get('agents', [])
                
                for agent in agents:
                    if agent.get('provider') == 'autogen_agentchat.agents.AssistantAgent':
                        ver = agent.get('version')
                        comp_ver = agent.get('component_version')
                        print(f"Gallery {row['id']} - Agent '{agent.get('label')}': Version={ver}, ComponentVersion={comp_ver}")
                        
                        if ver == 1:
                            print(f"  --> FOUND STALE V1 AGENT! Content: {str(agent)[:100]}...")

            except json.JSONDecodeError:
                pass
    except Exception as e:
        print(f"Error processing gallery: {e}")

    conn.close()

if __name__ == "__main__":
    check_gallery_versions()
