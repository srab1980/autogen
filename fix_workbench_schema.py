"""
Fix the workbench configuration with proper schema including 'provider' field
"""
import sqlite3
import json

DB_PATH = "autogen04202.db"

# Complete workbench with proper schema
COMPLETE_WORKBENCH = {
    "component_type": "workbench",
    "version": 1,
    "provider": "autogen_core.tools.StaticWorkbench",
    "label": "Exporter Workbench",
    "config": {
        "tools": [
            {
                "component_type": "tool",
                "version": 1,
                "provider": "autogen_core.tools.FunctionTool",
                "label": "Export To Word",
                "config": {
                    "name": "export_to_word",
                    "description": "Export content to Word document",
                    "source_code": '''from docx import Document
from datetime import datetime
import os

def export_to_word(content: str, title: str = "") -> dict:
    folder = "C:\\\\Users\\\\srab1.SAMEH-NVME\\\\Downloads\\\\AutoGen Studio Final\\\\AutoGen Studio\\\\AutoGen Studio\\\\Script"
    os.makedirs(folder, exist_ok=True)
    doc = Document()
    doc.add_heading("Rafeeq Export", 0)
    doc.add_paragraph(datetime.now().strftime("%Y-%m-%d %H:%M"))
    for line in str(content).splitlines():
        doc.add_paragraph(line)
    doc.save(os.path.join(folder, "Rafeeq_Export.docx"))
    return {"status": "ok"}
''',
                    "global_imports": [],
                    "has_cancellation_support": False
                }
            }
        ]
    }
}

def fix_workbench():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("=== FIXING WORKBENCH WITH PROPER SCHEMA ===")
    
    cursor.execute("SELECT id, component FROM team WHERE id = 4")
    row = cursor.fetchone()
    config = json.loads(row[1])
    
    participants = config.get('config', {}).get('participants', [])
    
    for participant in participants:
        agent_name = participant.get('config', {}).get('name', '')
        
        if agent_name == 'rafeeq_exporter':
            participant['config']['workbench'] = [COMPLETE_WORKBENCH]
            print(f"  ✓ Fixed workbench for {agent_name}")
    
    cursor.execute("UPDATE team SET component = ? WHERE id = ?", 
                  (json.dumps(config), 4))
    conn.commit()
    conn.close()
    
    print("\n✅ Done! Workbench now has proper 'provider' field.")

if __name__ == "__main__":
    fix_workbench()
