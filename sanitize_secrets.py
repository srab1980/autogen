
import os
import re

# Regex for OpenAI key (approximate)
key_pattern = re.compile(r'sk-proj-[a-zA-Z0-9_\-]+')

def sanitize_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if key_pattern.search(content):
            print(f"Sanitizing {filepath}...")
            new_content = key_pattern.sub('sk-proj-REDACTED', content)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
    except Exception:
        pass # Skip binary or decoding errors

for root, dirs, files in os.walk("."):
    if ".git" in dirs:
        dirs.remove(".git")
    if ".venv_new" in dirs:
        dirs.remove(".venv_new")
    if "autogen" in dirs: # Skip submodule/nested repo content if any
        dirs.remove("autogen") 
        
    for file in files:
        if file.endswith(".json") or file.endswith(".py") or file.endswith(".txt") or file.endswith(".md"):
            sanitize_file(os.path.join(root, file))
