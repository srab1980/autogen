import sqlite3
import json

conn = sqlite3.connect('autogen04202.db')
cursor = conn.cursor()

print("=== GALLERY MODELS ===")
cursor.execute('SELECT id, config FROM gallery')
for r in cursor.fetchall():
    cfg = json.loads(r[1])
    label = cfg.get('label', 'NO LABEL')
    model = cfg.get('config', {}).get('model', 'NO MODEL')
    print(f"Gallery {r[0]}: label='{label}', model='{model}'")

print("\n=== TEAM MODELS ===")
cursor.execute('SELECT id, component FROM team')
for team_id, blob in cursor.fetchall():
    cfg = json.loads(blob)
    print(f"\nTeam {team_id}: {cfg.get('label')}")
    # Find model_client configs
    def find_models(obj, path=""):
        if isinstance(obj, dict):
            if 'model_client' in obj:
                mc = obj['model_client']
                if isinstance(mc, dict):
                    label = mc.get('label', '')
                    model = mc.get('config', {}).get('model', 'NO MODEL')
                    print(f"  {path}: label='{label}', model='{model}'")
            for k, v in obj.items():
                find_models(v, f"{path}.{k}")
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                find_models(item, f"{path}[{i}]")
    find_models(cfg)

conn.close()
