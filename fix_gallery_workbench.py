import json
import os

def fix_workbench_to_single(config, path="root"):
    """Recursively convert workbench arrays to single objects"""
    changes = []
    
    if isinstance(config, dict):
        # Check for workbench in config
        if 'config' in config and isinstance(config['config'], dict):
            inner_config = config['config']
            if 'workbench' in inner_config:
                wb = inner_config['workbench']
                if isinstance(wb, list):
                    if len(wb) == 1:
                        inner_config['workbench'] = wb[0]
                        changes.append(f"Converted workbench array to single at {path}")
                    elif len(wb) == 0:
                        del inner_config['workbench']
                        changes.append(f"Removed empty workbench array at {path}")
                    else:
                        inner_config['workbench'] = wb[0]
                        changes.append(f"WARNING: Multiple workbenches at {path}, using first")
        
        # Recursively process all keys
        for key, value in config.items():
            if isinstance(value, (dict, list)):
                changes.extend(fix_workbench_to_single(value, f"{path}.{key}"))
    
    elif isinstance(config, list):
        for i, item in enumerate(config):
            changes.extend(fix_workbench_to_single(item, f"{path}[{i}]"))
    
    return changes

# Path to the default gallery
gallery_path = r"autogen\python\packages\autogen-studio\frontend\src\components\views\gallery\default_gallery.json"

with open(gallery_path, 'r', encoding='utf-8') as f:
    gallery = json.load(f)

print("Processing default_gallery.json...")

changes = fix_workbench_to_single(gallery)

if changes:
    print(f"\nMade {len(changes)} changes:")
    for change in changes:
        print(f"  {change}")
    
    with open(gallery_path, 'w', encoding='utf-8') as f:
        json.dump(gallery, f, indent=2, ensure_ascii=False)
    
    print(f"\nSaved updated gallery!")
else:
    print("No changes needed")

print("Done!")
