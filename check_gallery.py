"""Check Gallery for cached export tools and fix them"""
import sqlite3
import json

conn = sqlite3.connect('autogen04202.db')
cursor = conn.cursor()

# Simple minimal export
MINIMAL = '''from docx import Document
from datetime import datetime
import os

DATA = []

def export_to_word(content: str, title: str = "") -> dict:
    global DATA
    DATA.append({"time": datetime.now().strftime("%H:%M:%S"), "text": str(content)})
    
    folder = "C:\\\\Users\\\\srab1.SAMEH-NVME\\\\Downloads\\\\AutoGen Studio Final\\\\AutoGen Studio\\\\AutoGen Studio\\\\Script"
    os.makedirs(folder, exist_ok=True)
    
    doc = Document()
    doc.add_heading("Rafeeq Report", 0)
    for entry in DATA:
        doc.add_heading(entry["time"], 1)
        for line in entry["text"].splitlines():
            doc.add_paragraph(line)
    
    path = os.path.join(folder, "Rafeeq_Report.docx")
    doc.save(path)
    return {"status": "ok", "count": len(DATA)}
'''

print("=== CHECKING AND FIXING GALLERY ===")

# Check Gallery
cursor.execute("SELECT id, config FROM gallery")
for row_id, config_blob in cursor.fetchall():
    config = json.loads(config_blob)
    config_str = json.dumps(config)
    
    # Check for 'para' in source code
    if 'def _set_rtl(para)' in config_str or 'def set_arabic_rtl(para' in config_str:
        print(f"Gallery {row_id}: Found 'para' parameter!")
        
    # Check for export tools
    if config.get('component_type') == 'tool':
        label = config.get('label', '')
        if 'export' in label.lower() or 'word' in label.lower():
            print(f"Gallery {row_id}: Export tool '{label}'")
            if 'config' in config and 'source_code' in config['config']:
                old_code = config['config']['source_code']
                if 'para' in old_code and 'paragraph' not in old_code:
                    print(f"  -> Has 'para' variable, FIXING...")
                    config['config']['source_code'] = MINIMAL
                    cursor.execute("UPDATE gallery SET config = ? WHERE id = ?",
                                  (json.dumps(config), row_id))
                    print(f"  -> Fixed!")

conn.commit()

# Also check sessions table for cached runs
print("\n=== CHECKING SESSIONS ===")
cursor.execute("SELECT COUNT(*) FROM session")
session_count = cursor.fetchone()[0]
print(f"Sessions: {session_count}")

conn.close()
print("\n✅ Done checking!")
