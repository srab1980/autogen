"""Find function parameters that could cause KeyError"""
import sqlite3
import json
import re

conn = sqlite3.connect('autogen04202.db')
cursor = conn.cursor()

cursor.execute("SELECT component FROM team WHERE id = 4")
config_str = cursor.fetchone()[0]

# Search for function definitions with parameters
print("=== SEARCHING FOR PROBLEMATIC FUNCTION PARAMETERS ===\n")

# Find all function definitions
func_pattern = r'def\s+\w+\s*\([^)]*\)'
matches = re.findall(func_pattern, config_str)

for match in matches:
    # Check if it has 'para' as a parameter (not 'paragraph')
    if 'para' in match.lower():
        print(f"FOUND: {match}")

# Also search for the _set_rtl or set_arabic_rtl functions
rtl_pattern = r'def\s+(set_arabic_rtl|_set_rtl)\s*\([^)]*\)'
rtl_matches = re.findall(rtl_pattern, config_str)
print(f"\nRTL functions found: {rtl_matches}")

# Search for any (para) parameter pattern
para_param = r'\(\s*para\s*[,)]'
para_matches = re.findall(para_param, config_str)
print(f"\nParameters with 'para': {para_matches}")

# Let's look for the exact problematic pattern
problem_pattern = r'def\s+\w+\s*\(\s*para\b'
problem_matches = re.findall(problem_pattern, config_str)
print(f"\nFunctions with 'para' as first param: {problem_matches}")

conn.close()
