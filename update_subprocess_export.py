"""
Use subprocess approach - the export tool just calls the external script
This avoids all type introspection issues with complex code
"""
import sqlite3
import json

DB_PATH = "autogen04202.db"

# Ultra minimal export - just calls external script
SUBPROCESS_EXPORT = '''import subprocess
import os

def export_to_word(content: str, title: str = "") -> dict:
    """Export by calling external Python script."""
    try:
        script_path = os.path.join(
            "C:\\\\Users\\\\srab1.SAMEH-NVME\\\\Downloads\\\\AutoGen Studio Final\\\\AutoGen Studio\\\\AutoGen Studio",
            "export_complete_dialogue.py"
        )
        
        result = subprocess.run(
            ["python", script_path],
            capture_output=True,
            text=True,
            cwd="C:\\\\Users\\\\srab1.SAMEH-NVME\\\\Downloads\\\\AutoGen Studio Final\\\\AutoGen Studio\\\\AutoGen Studio"
        )
        
        if result.returncode == 0:
            return {"status": "ok", "output": result.stdout}
        else:
            return {"status": "error", "error": result.stderr}
            
    except Exception as err:
        return {"status": "error", "message": str(err)}
'''

def update_exporter_tool():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("=== USING SUBPROCESS APPROACH ===")
    
    cursor.execute("SELECT id, component FROM team WHERE id = 4")
    row = cursor.fetchone()
    config = json.loads(row[1])
    
    participants = config.get('config', {}).get('participants', [])
    
    for participant in participants:
        agent_name = participant.get('config', {}).get('name', '')
        
        if agent_name == 'rafeeq_exporter':
            workbenches = participant.get('config', {}).get('workbench', [])
            for wb in workbenches:
                tools = wb.get('config', {}).get('tools', [])
                for tool in tools:
                    if 'config' in tool:
                        tool['config']['source_code'] = SUBPROCESS_EXPORT
                        print(f"  ✓ Updated to subprocess approach on {agent_name}")
    
    cursor.execute("UPDATE team SET component = ? WHERE id = ?", 
                  (json.dumps(config), 4))
    conn.commit()
    conn.close()
    
    print("\n✅ Now uses subprocess to call external export script!")

if __name__ == "__main__":
    update_exporter_tool()
