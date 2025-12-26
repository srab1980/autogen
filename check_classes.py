
try:
    from autogen_core.tools import StaticWorkbench
    print("Found autogen_core.tools.StaticWorkbench")
except ImportError as e:
    print(f"Missing autogen_core.tools.StaticWorkbench: {e}")

try:
    from autogen_ext.tools import FunctionTool
    print("Found autogen_ext.tools.FunctionTool")
except ImportError as e:
    print(f"Missing autogen_ext.tools.FunctionTool: {e}")
