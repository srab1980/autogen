import sqlite3
import json

DB_FILE = "/app/data/autogen04202.db"

def check_versions():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    print("Checking Gallery Table...")
    rows = cursor.execute("SELECT id, config, user_id FROM gallery").fetchall()
    
    v1_count = 0
    v2_count = 0
    
    for row in rows:
        try:
            config = json.loads(row['config'])
            if 'components' not in config:
                continue
            
            components = config['components']
            agents = components.get('agents', [])
            
            for agent in agents:
                label = agent.get('label') or agent.get('config', {}).get('name')
                
                # Check top-level version (if component_version exists)
                # or nested in config? 
                # serialization usually puts 'version' at top level for ComponentModel
                
                version = agent.get('version')
                provider = agent.get('provider')
                if version == 2 and provider == "autogen_agentchat.agents.AssistantAgent":
                    print(f"DUMP AGENT {row['id']}: {json.dumps(agent, indent=2)}")
                    return # Just dump one and exit to avoid spam

            # Check inside Teams
            teams = components.get('teams', [])
            for team in teams:
                 participants = team.get('config', {}).get('participants', [])
                 # config might be flat or nested depending on serialization
                 if not participants:
                     participants = team.get('participants', []) # Support both legacy/new formats?

                 for agent in participants:
                    label = agent.get('label') or agent.get('config', {}).get('name') or "Unknown"
                    version = agent.get('version')
                    provider = agent.get('provider')
                    if version == 1 and "AssistantAgent" in str(provider):
                        print(f"Gallery {row['id']} - Team Agent '{label}': Version {version}, Provider: {provider}")
                        v1_count += 1
                    elif version == 2 and "AssistantAgent" in str(provider):
                        v2_count += 1
                    
        except Exception as e:
            print(f"Error parsing row {row['id']}: {e}")

    print(f"\nSummary: v1={v1_count}, v2={v2_count}")
    conn.close()

if __name__ == "__main__":
    check_versions()
