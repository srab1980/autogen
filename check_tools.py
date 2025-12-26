"""Check what's actually in the export tools"""
import sqlite3
import json

conn = sqlite3.connect('autogen04202.db')
cursor = conn.cursor()

cursor.execute("SELECT component FROM team WHERE id = 4")
config = json.loads(cursor.fetchone()[0])

print("=== CHECKING ALL TOOLS IN RAFEEQ2 ===\n")

for i, participant in enumerate(config.get('config', {}).get('participants', [])):
    agent_name = participant.get('config', {}).get('name', 'unknown')
    workbenches = participant.get('config', {}).get('workbench', [])
    
    for wb in workbenches:
        tools = wb.get('config', {}).get('tools', [])
        for tool in tools:
            label = tool.get('label', 'no label')
            source = tool.get('config', {}).get('source_code', '')
            
            print(f"Agent {i}: {agent_name}")
            print(f"  Tool: {label}")
            print(f"  Code preview: {source[:150]}...")
            
            # Check for problematic variable names
            if 'para' in source and 'paragraph' not in source:
                print("  ⚠️ FOUND 'para' without 'paragraph'!")
            if 'def export_to_word' in source:
                # Extract function signature
                import re
                sig = re.search(r'def export_to_word\([^)]+\)', source)
                if sig:
                    print(f"  Signature: {sig.group()}")
            print()

conn.close()
