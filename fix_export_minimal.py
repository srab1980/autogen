"""
Ultra minimal export tool - absolute minimum code to avoid type introspection issues
"""
import sqlite3
import json

DB_PATH = "autogen04202.db"

# The most minimal possible export tool
MINIMAL_CODE = '''from docx import Document
from datetime import datetime
import os

ALL_DATA = []

def export_to_word(content: str, title: str = "") -> dict:
    """Export to Word."""
    global ALL_DATA
    
    ALL_DATA.append({"t": datetime.now().strftime("%H:%M:%S"), "c": str(content)})
    
    folder = "C:\\\\Users\\\\srab1.SAMEH-NVME\\\\Downloads\\\\AutoGen Studio Final\\\\AutoGen Studio\\\\AutoGen Studio\\\\Script"
    os.makedirs(folder, exist_ok=True)
    
    doc = Document()
    doc.add_heading("تقرير رفيق", 0)
    doc.add_paragraph(datetime.now().strftime("%Y-%m-%d %H:%M"))
    doc.add_page_break()
    
    for entry in ALL_DATA:
        doc.add_heading(entry["t"], 1)
        for line in entry["c"].splitlines():
            doc.add_paragraph(line)
        doc.add_paragraph("─" * 40)
    
    path = os.path.join(folder, "Rafeeq_Report.docx")
    doc.save(path)
    
    return {"status": "ok", "path": path, "count": len(ALL_DATA)}
'''

def update_all_export_tools():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("=== APPLYING ULTRA-MINIMAL EXPORT TOOL ===")
    
    # Fix team 4
    cursor.execute("SELECT id, component FROM team WHERE id = 4")
    row = cursor.fetchone()
    if row:
        config = json.loads(row[1])
        fixed = fix_tools(config, "team4")
        if fixed:
            cursor.execute("UPDATE team SET component = ? WHERE id = ?", 
                          (json.dumps(config), 4))
            print("  ✓ Team 4 updated")
    
    conn.commit()
    conn.close()
    print("\n✅ All export tools updated with minimal code!")

def fix_tools(obj, path=""):
    fixed = False
    
    if isinstance(obj, dict):
        # Check if this is ANY tool (not just Export To Word)
        if obj.get('component_type') == 'tool':
            tool_name = obj.get('label', '') or obj.get('config', {}).get('name', '')
            if 'export' in str(tool_name).lower() or 'word' in str(tool_name).lower():
                print(f"  Found: {tool_name} at {path}")
                if 'config' in obj:
                    obj['config']['source_code'] = MINIMAL_CODE
                    obj['config']['name'] = 'export_to_word'
                    fixed = True
        
        for key, val in obj.items():
            if fix_tools(val, f"{path}.{key}"):
                fixed = True
                
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            if fix_tools(item, f"{path}[{i}]"):
                fixed = True
    
    return fixed

if __name__ == "__main__":
    update_all_export_tools()
