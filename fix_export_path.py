"""
Fix Export To Word tool with proper absolute path
"""
import sqlite3
import json

DB_PATH = "autogen04202.db"

# Fixed export tool with correct absolute path
NEW_SOURCE_CODE = '''from docx import Document
from datetime import datetime
import os

def export_to_word(content: str, title: str = "") -> dict:
    """
    Export content to Word file.
    
    Parameters:
        content: The content to export
        title: Optional title
    
    Returns:
        dict with status
    """
    try:
        # Use absolute path directly
        folder = "C:\\\\Users\\\\srab1.SAMEH-NVME\\\\Downloads\\\\AutoGen Studio Final\\\\AutoGen Studio\\\\AutoGen Studio\\\\Script"
        os.makedirs(folder, exist_ok=True)
        
        fname = "Rafeeq_Report.docx"
        fpath = os.path.join(folder, fname)
        
        # Always create new document to avoid corruption
        doc = Document()
        doc.add_heading("تقرير رفيق", level=0)
        doc.add_paragraph(datetime.now().strftime("%Y-%m-%d %H:%M"))
        doc.add_page_break()
        
        if title:
            doc.add_heading(str(title), level=1)
        else:
            doc.add_heading(datetime.now().strftime("Section %H:%M:%S"), level=1)
        
        txt = str(content)
        for ln in txt.splitlines():
            if ln.startswith("# "):
                doc.add_heading(ln[2:], level=2)
            elif ln.startswith("## "):
                doc.add_heading(ln[3:], level=3)
            elif ln.startswith("- "):
                doc.add_paragraph(ln[2:], style="List Bullet")
            elif ln.strip():
                doc.add_paragraph(ln)
        
        doc.add_paragraph("")
        doc.add_paragraph("─" * 40)
        
        doc.save(fpath)
        
        return {"file_name": fname, "file_path": fpath, "status": "ok"}
    except Exception as err:
        return {"status": "error", "message": str(err)}
'''

def fix_all_tools(obj):
    changed = False
    
    if isinstance(obj, dict):
        if obj.get('component_type') == 'tool':
            lbl = obj.get('label', '')
            if 'export' in lbl.lower() or 'word' in lbl.lower():
                if 'config' in obj and 'source_code' in obj['config']:
                    print(f"  Fixing: {lbl}")
                    obj['config']['source_code'] = NEW_SOURCE_CODE
                    obj['config']['name'] = 'export_to_word'
                    changed = True
        
        for k, v in obj.items():
            if fix_all_tools(v):
                changed = True
    
    elif isinstance(obj, list):
        for itm in obj:
            if fix_all_tools(itm):
                changed = True
    
    return changed

def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    print("=== FIXING EXPORT WITH ABSOLUTE PATH ===")
    
    cur.execute("SELECT id, component FROM team WHERE id = 4")
    row = cur.fetchone()
    if row:
        cfg = json.loads(row[1])
        if fix_all_tools(cfg):
            cur.execute("UPDATE team SET component = ? WHERE id = ?", 
                       (json.dumps(cfg), 4))
            print("  ✓ Rafeeq2 UPDATED")
    
    conn.commit()
    conn.close()
    print("\n✅ Done!")

if __name__ == "__main__":
    main()
