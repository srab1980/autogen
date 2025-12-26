import asyncio
import json
from autogen_core import ComponentModel
try:
    from autogenstudio.validation.validation_service import ValidationService
    from autogen_agentchat.agents import AssistantAgent
except ImportError as e:
    print(e)
    exit(1)

# Mimic the config from default_gallery.json (Agent 0)
config_dict = {
  "provider": "autogen_agentchat.agents.AssistantAgent",
  "component_type": "agent",
  "version": 2,
  "component_version": 2,
  "description": "An agent that provides assistance with ability to use tools.",
  "label": "AssistantAgent",
  "config": {
    "name": "assistant_agent",
    "model_client": {
      "provider": "autogen_ext.models.openai.OpenAIChatCompletionClient",
      "component_type": "model",
      "version": 1,
      "component_version": 1,
      "config": {
        "model": "gpt-4o-mini"
      }
    },
    "workbench": {
      "provider": "autogen_core.tools.StaticWorkbench",
      "component_type": "workbench",
      "version": 1,
      "component_version": 1,
      "config": {
        "tools": [
          {
            "provider": "autogen_core.tools.FunctionTool",
            "component_type": "tool",
            "version": 1,
            "component_version": 1,
            "config": {
              "source_code": "def calculator(a: float, b: float, operator: str) -> str: return '0'",
              "name": "calculator",
              "description": "calc",
              "global_imports": [],
              "has_cancellation_support": False
            }
          }
        ]
      }
    }
  }
}

async def main():
    print("Testing instantiation...")
    try:
        model = ComponentModel(**config_dict)
        # Validate
        res = ValidationService.validate(model)
        if not res.is_valid:
            print("Validation FAILED:")
            for err in res.errors:
                print(f"  {err.error}")
        else:
            print("Validation PASSED (Schema Check)")
            # Try instantiation if validation only checks schema
            # validate() calls validate_instantiation() too.
            
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    asyncio.run(main())
