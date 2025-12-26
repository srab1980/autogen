import os
from bs4 import BeautifulSoup

file_path = r".venv_new\Lib\site-packages\autogenstudio\web\ui\index.html"

if os.path.exists(file_path):
    print(f"Reading {file_path}")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        soup = BeautifulSoup(content, 'html.parser')
        scripts = soup.find_all('script')
        for script in scripts:
            src = script.get('src')
            if src:
                print(f"Script src: {src}")
else:
    print(f"File not found: {file_path}")

# Also list top 5 js files in that dir
js_dir = os.path.dirname(file_path)
print(f"\nJS files in {js_dir}:")
js_files = [f for f in os.listdir(js_dir) if f.endswith('.js')]
for f in js_files[:5]:
    print(f"  {f}")
