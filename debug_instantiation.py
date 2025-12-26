import sqlite3
import json
import asyncio
import os

try:
    from autogen_core import ComponentModel
    from autogenstudio.validation.validation_service import ValidationService
except ImportError as e:
    print(f"Import Error: {e}")
    exit(1)

log_file = open("debug_instantiation.log", "w", encoding="utf-8")

def log(msg):
    print(msg)
    log_file.write(msg + "\n")

def check_db_components():
    db_path = 'autogen04202.db'
    if not os.path.exists(db_path):
        log(f"Database not found at {db_path}")
        return

    log(f"Connecting to {db_path}...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check Teams
    try:
        cursor.execute("SELECT id, component FROM team")
        rows = cursor.fetchall()
        log(f"Found {len(rows)} teams.")
        for row in rows:
            tid, config_str = row
            label = "Unknown"
            
            try:
                config = json.loads(config_str)
                label = config.get("label", "Unknown")
                model = ComponentModel(**config)
                
                response = ValidationService.validate(model)
                if not response.is_valid:
                    log(f"FAIL: Team {tid} ({label})")
                    for err in response.errors:
                        log(f"  Error: {err.error}")
                        if "Tools cannot be used with a workbench" in err.error:
                             log("  !!! FOUND THE CULPRIT IN TEAM !!!")
            except Exception as e:
                log(f"ERROR: Parsing Team {tid}: {e}")
    except Exception as e:
        log(f"Error checking teams: {e}")

    # Check Gallery
    try:
        cursor.execute("PRAGMA table_info(gallery)")
        if 'config' in [c[1] for c in cursor.fetchall()]:
             cursor.execute("SELECT id, config FROM gallery")
             rows = cursor.fetchall()
             log(f"Found {len(rows)} galleries.")
             for row in rows:
                 gid, config_str = row
                 if not config_str: continue
                 try:
                     gal_data = json.loads(config_str)
                     if "components" in gal_data and "agents" in gal_data["components"]:
                         for i, agent_conf in enumerate(gal_data["components"]["agents"]):
                             try:
                                 # Convert dict to ComponentModel manually if needed or pass to validate
                                 # agent_conf is a dict.
                                 model = ComponentModel(**agent_conf)
                                 response = ValidationService.validate(model)
                                 if not response.is_valid:
                                     label = agent_conf.get('label', 'Unknown')
                                     log(f"FAIL: Gallery {gid} Agent {i} ({label})")
                                     for err in response.errors:
                                         log(f"  Error: {err.error}")
                                     if "Tools cannot be used with a workbench" in str(response.errors):
                                         log("  !!! FOUND THE CULPRIT IN GALLERY !!!")
                             except Exception as e:
                                 # log(f"Error validating gallery agent {i}: {e}")
                                 pass
                 except Exception as e:
                     log(f"Error parsing gallery {gid}: {e}")

    except Exception as e:
        log(f"Error checking gallery: {e}")

    conn.close()
    log_file.close()

if __name__ == "__main__":
    check_db_components()
