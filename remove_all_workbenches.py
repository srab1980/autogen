"""
Remove ALL workbenches/tools from all agents except rafeeq_exporter
The workflow can run without tools - agents don't need them
"""
import sqlite3
import json

DB_PATH = "autogen04202.db"

# Minimal export for exporter only
MINIMAL_EXPORT = '''from docx import Document
from datetime import datetime
import os

def export_to_word(content: str, title: str = "") -> dict:
    folder = "C:\\\\Users\\\\srab1.SAMEH-NVME\\\\Downloads\\\\AutoGen Studio Final\\\\AutoGen Studio\\\\AutoGen Studio\\\\Script"
    os.makedirs(folder, exist_ok=True)
    doc = Document()
    doc.add_heading("Rafeeq Report", 0)
    for line in str(content).splitlines():
        doc.add_paragraph(line)
    doc.save(os.path.join(folder, "Rafeeq_Report.docx"))
    return {"status": "ok"}
'''

def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("=== REMOVING ALL WORKBENCHES EXCEPT EXPORTER ===")
    
    cursor.execute("SELECT id, component FROM team WHERE id = 4")
    row = cursor.fetchone()
    config = json.loads(row[1])
    
    participants = config.get('config', {}).get('participants', [])
    
    for i, participant in enumerate(participants):
        agent_name = participant.get('config', {}).get('name', '')
        
        if agent_name == 'rafeeq_exporter':
            # Keep workbench but simplify tools
            workbenches = participant.get('config', {}).get('workbench', [])
            for wb in workbenches:
                tools = wb.get('config', {}).get('tools', [])
                for tool in tools:
                    if 'config' in tool:
                        tool['config']['source_code'] = MINIMAL_EXPORT
                        print(f"  ✓ Simplified export tool on {agent_name}")
        else:
            # Remove workbench entirely
            if 'workbench' in participant.get('config', {}):
                del participant['config']['workbench']
                print(f"  ✗ Removed workbench from {agent_name}")
    
    cursor.execute("UPDATE team SET component = ? WHERE id = ?", 
                  (json.dumps(config), 4))
    conn.commit()
    conn.close()
    
    print("\n✅ Done! Only rafeeq_exporter has a workbench/tools now.")

if __name__ == "__main__":
    main()
