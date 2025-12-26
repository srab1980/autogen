
import importlib
import pkgutil

def check_module(module_name):
    print(f"Checking {module_name}...")
    try:
        module = importlib.import_module(module_name)
        print(f" - Found: {module.__file__}")
        if hasattr(module, "__path__"):
             for importer, modname, ispkg in pkgutil.iter_modules(module.__path__):
                print(f"   - {modname}")
    except ImportError as e:
        print(f" - Import Error: {e}")

check_module("autogen_ext")
check_module("autogen")
