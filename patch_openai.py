
import os

file_path = r"c:\Users\srab1.SAMEH-NVME\Downloads\AutoGen Studio Final\AutoGen Studio\AutoGen Studio\.venv_new\Lib\site-packages\autogen_ext\models\openai\_openai_client.py"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

target_str = """        if len(converted_tools) > 0:
            # Convert to OpenAI format and add to create_args
            converted_tool_choice = convert_tool_choice(tool_choice)
            create_args["tool_choice"] = converted_tool_choice

        return CreateParams("""

patch_str = """        if len(converted_tools) > 0:
            # Convert to OpenAI format and add to create_args
            converted_tool_choice = convert_tool_choice(tool_choice)
            create_args["tool_choice"] = converted_tool_choice

        # PATCH: Filter out stop param for gpt-5/o1 models
        if "stop" in create_args:
            model_name = create_args.get("model", "")
            if any(x in model_name.lower() for x in ["gpt-5", "o1-", "preview"]):
                if "stop" in create_args:
                    del create_args["stop"]

        return CreateParams("""

if patch_str.strip() in content:
    print("Already patched.")
else:
    new_content = content.replace(target_str, patch_str)
    if new_content == content:
        print("Target string not found!")
    else:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("Successfully patched.")
