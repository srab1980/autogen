
import sys
import os
# Add the autogen-studio package to path so we can import from it
sys.path.append(r"c:\Users\srab1.SAMEH-NVME\Downloads\AutoGen Studio Final\AutoGen Studio\AutoGen Studio\autogen\python\packages\autogen-studio")

try:
    from autogenstudio.gallery.tools.calculator import calculator_tool
    print(calculator_tool.dump_component().model_dump_json(indent=2))
except Exception as e:
    print(f"Error: {e}")
