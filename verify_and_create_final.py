import json
import os
import shutil

source_file = 'rafeeq_complete_import.json'
target_file = 'rafeeq_final_v3.json'

try:
    with open(source_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    participants = data.get('config', {}).get('participants', [])
    print(f"Scanning {len(participants)} participants...")
    
    errors_found = 0
    for i, p in enumerate(participants):
         name = p.get('config', {}).get('name', 'Unknown')
         workbench = p.get('config', {}).get('workbench')
         
         if isinstance(workbench, list):
             print(f"ERROR: Participant {i} ({name}) has workbench as LIST!")
             errors_found += 1
             # Fix it again just in case
             if workbench:
                 p['config']['workbench'] = workbench[0]
             else:
                 p['config']['workbench'] = None
         elif isinstance(workbench, dict) or workbench is None:
             pass # Dict is good
         else:
             print(f"WARNING: Participant {i} ({name}) has workbench as {type(workbench)}")

    if errors_found == 0:
        print("Verification PASS: All workbenches are dicts or None.")
    else:
        print(f"Verification FAIL: Found {errors_found} errors. Fixing...")

    # Save to new file
    with open(target_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Saved to {os.path.abspath(target_file)}")

except Exception as e:
    print(f"Error: {e}")
