import os
import requests
from bs4 import BeautifulSoup

def list_index_htmls(start_path):
    print(f"Searching in {start_path}")
    for root, dirs, files in os.walk(start_path):
        for file in files:
            if file == "index.html":
                print(f"Found: {os.path.join(root, file)}")

def fetch_and_parse(url):
    try:
        print(f"\nFetching {url}...")
        response = requests.get(url)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            scripts = soup.find_all('script')
            print("Scripts found:")
            for script in scripts:
                src = script.get('src')
                if src:
                    print(f"  src: {src}")
                else:
                    print("  (inline script)")
    except Exception as e:
        print(f"Error fetching {url}: {e}")

ui_path = r"c:\Users\srab1\Downloads\AutoGen Studio\AutoGen Studio\autogen\python\packages\autogen-studio\autogenstudio\web\ui"
list_index_htmls(ui_path)

fetch_and_parse("http://127.0.0.1:8081/")
fetch_and_parse("http://127.0.0.1:8081/build/")
