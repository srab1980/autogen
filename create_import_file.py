import json
import os

source_file = 'rafeeq_team_config_fixed.json'
target_file = 'rafeeq_complete_import.json'
api_key = "sk-proj-REDACTED"

try:
    with open(source_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Validate agent list
    participants = data.get('config', {}).get('participants', [])
    print(f"Found {len(participants)} participants:")
    for p in participants:
         print(f"- {p.get('config', {}).get('name')}")
         
         # Inject API Key
         try:
             # Handle different structures
             model_client = p.get('config', {}).get('model_client', {})
             if model_client:
                 if 'config' not in model_client:
                     model_client['config'] = {}
                 model_client['config']['api_key'] = api_key
                 print(f"  -> Injected API key for {p.get('config', {}).get('name')}")
             
             # Fix Workbench (List to Dict)
             workbench = p.get('config', {}).get('workbench')
             if isinstance(workbench, list):
                 if workbench:
                    p['config']['workbench'] = workbench[0]
                    print(f"  -> Fixed workbench (list -> dict) for {p.get('config', {}).get('name')}")
                 else:
                    p['config']['workbench'] = None
             
         except Exception as e:
             print(f"  -> Failed to update {p.get('name')}: {e}")

    with open(target_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\nSuccessfully created {target_file} at {os.path.abspath(target_file)}")

except Exception as e:
    print(f"Error: {e}")
