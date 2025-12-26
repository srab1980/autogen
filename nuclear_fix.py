"""
NUCLEAR OPTION: Remove ALL export tools except one minimal one on exporter agent
"""
import sqlite3
import json

DB_PATH = "autogen04202.db"

# Absolute minimal export - no helper functions, no complex types
NUCLEAR_MINIMAL = '''from docx import Document
from datetime import datetime
import os

ITEMS = []

def export_to_word(content: str, title: str = "") -> dict:
    global ITEMS
    ITEMS.append(str(content))
    
    folder = "C:\\\\Users\\\\srab1.SAMEH-NVME\\\\Downloads\\\\AutoGen Studio Final\\\\AutoGen Studio\\\\AutoGen Studio\\\\Script"
    os.makedirs(folder, exist_ok=True)
    
    doc = Document()
    doc.add_heading("Rafeeq Report", 0)
    doc.add_paragraph(datetime.now().strftime("%Y-%m-%d %H:%M"))
    
    for item in ITEMS:
        doc.add_paragraph("---")
        for line in item.splitlines():
            doc.add_paragraph(line)
    
    doc.save(os.path.join(folder, "Rafeeq_Report.docx"))
    return {"status": "ok"}
'''

def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("=== NUCLEAR OPTION: REMOVING ALL EXTRA EXPORT TOOLS ===")
    
    cursor.execute("SELECT id, component FROM team WHERE id = 4")
    row = cursor.fetchone()
    config = json.loads(row[1])
    
    participants = config.get('config', {}).get('participants', [])
    
    for i, participant in enumerate(participants):
        agent_name = participant.get('config', {}).get('name', '')
        workbenches = participant.get('config', {}).get('workbench', [])
        
        for wb in workbenches:
            tools = wb.get('config', {}).get('tools', [])
            
            # Filter out export tools from non-exporter agents
            # Keep only on rafeeq_exporter (agent 15)
            new_tools = []
            for tool in tools:
                label = tool.get('label', '')
                if 'export' in label.lower() or 'word' in label.lower():
                    if agent_name == 'rafeeq_exporter':
                        # Keep and update with minimal code
                        tool['config']['source_code'] = NUCLEAR_MINIMAL
                        new_tools.append(tool)
                        print(f"  ✓ Keeping export on {agent_name}")
                    else:
                        print(f"  ✗ Removing export from {agent_name}")
                else:
                    new_tools.append(tool)
            
            wb['config']['tools'] = new_tools
    
    # Save
    cursor.execute("UPDATE team SET component = ? WHERE id = ?", 
                  (json.dumps(config), 4))
    conn.commit()
    conn.close()
    
    print("\n✅ Done! Only rafeeq_exporter has export tool now.")

if __name__ == "__main__":
    main()
