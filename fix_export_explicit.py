"""
Fix Export To Word tool - using explicit variable names
"""
import sqlite3
import json

DB_PATH = "autogen04202.db"

# Export tool with explicit variable names - no 'p' or short names
NEW_SOURCE_CODE = '''from docx import Document
from datetime import datetime
import os

def export_to_word(report_markdown, section_title=None):
    """
    Export content to Word file.
    
    Args:
        report_markdown: The markdown content to export
        section_title: Optional title for the section
    
    Returns:
        Dictionary with file info and status
    """
    try:
        # Build output path
        output_folder = os.path.join(
            "C:", os.sep, "Users", "srab1.SAMEH-NVME", "Downloads",
            "AutoGen Studio Final", "AutoGen Studio", "AutoGen Studio", "Script"
        )
        os.makedirs(output_folder, exist_ok=True)
        
        output_file = "Rafeeq_Report.docx"
        full_path = os.path.join(output_folder, output_file)
        
        # Create or open document
        if os.path.exists(full_path):
            word_doc = Document(full_path)
            word_doc.add_page_break()
        else:
            word_doc = Document()
            word_doc.add_heading("تقرير رفيق", level=0)
            word_doc.add_paragraph(datetime.now().strftime("%Y-%m-%d %H:%M"))
            word_doc.add_page_break()
        
        # Section header
        if section_title:
            word_doc.add_heading(str(section_title), level=1)
        else:
            word_doc.add_heading(datetime.now().strftime("Section %H:%M:%S"), level=1)
        
        # Content
        content_text = str(report_markdown)
        for content_line in content_text.splitlines():
            if content_line.startswith("# "):
                word_doc.add_heading(content_line[2:], level=2)
            elif content_line.startswith("## "):
                word_doc.add_heading(content_line[3:], level=3)
            elif content_line.startswith("- "):
                word_doc.add_paragraph(content_line[2:], style="List Bullet")
            elif content_line.strip():
                word_doc.add_paragraph(content_line)
        
        word_doc.add_paragraph("")
        word_doc.add_paragraph("─" * 40)
        
        word_doc.save(full_path)
        
        return {
            "file_name": output_file,
            "file_path": full_path,
            "status": "ok"
        }
    except Exception as error:
        return {"status": "error", "message": str(error)}
'''

def fix_all_tools(config_obj):
    """Fix all export tools"""
    changed = False
    
    if isinstance(config_obj, dict):
        if config_obj.get('component_type') == 'tool':
            tool_label = config_obj.get('label', '')
            if 'export' in tool_label.lower() or 'word' in tool_label.lower():
                if 'config' in config_obj and 'source_code' in config_obj['config']:
                    print(f"  Fixing: {tool_label}")
                    config_obj['config']['source_code'] = NEW_SOURCE_CODE
                    config_obj['config']['name'] = 'export_to_word'
                    changed = True
        
        for key_name, value_obj in config_obj.items():
            if fix_all_tools(value_obj):
                changed = True
    
    elif isinstance(config_obj, list):
        for item_obj in config_obj:
            if fix_all_tools(item_obj):
                changed = True
    
    return changed

def main():
    db_conn = sqlite3.connect(DB_PATH)
    db_cursor = db_conn.cursor()
    
    print("=== FIXING EXPORT TOOL (explicit variable names) ===")
    
    db_cursor.execute("SELECT id, component FROM team WHERE id = 4")
    team_row = db_cursor.fetchone()
    if team_row:
        team_config = json.loads(team_row[1])
        if fix_all_tools(team_config):
            db_cursor.execute("UPDATE team SET component = ? WHERE id = ?", 
                             (json.dumps(team_config), 4))
            print("  ✓ Rafeeq2 UPDATED")
    
    db_conn.commit()
    db_conn.close()
    print("\n✅ Export tool fixed with explicit variable names!")

if __name__ == "__main__":
    main()
