from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.tools import FunctionTool
from autogen_core.tools import StaticStreamWorkbench, StaticWorkbench
from autogen_ext.agents.web_surfer import MultimodalWebSurfer
from autogen_agentchat.teams import RoundRobinGroupChat, SelectorGroupChat

try:
    print(f"AssistantAgent: {AssistantAgent.component_version}")
except:
    print("AssistantAgent: Error checking version")

try:
    print(f"UserProxyAgent: {UserProxyAgent.component_version}")
except:
    print("UserProxyAgent: Error checking version")

try:
    print(f"OpenAIChatCompletionClient: {OpenAIChatCompletionClient.component_version}")
except:
    print("OpenAIChatCompletionClient: Error checking version")

try:
    print(f"FunctionTool: {FunctionTool.component_version}")
except:
    print("FunctionTool: Error checking version")
    
try:
    print(f"StaticStreamWorkbench: {StaticStreamWorkbench.component_version}")
except:
    print("StaticStreamWorkbench: Error checking version")

try:
    print(f"StaticWorkbench: {StaticWorkbench.component_version}")
except:
    print("StaticWorkbench: Error checking version")

try:
    print(f"MultimodalWebSurfer: {MultimodalWebSurfer.component_version}")
except:
    print("MultimodalWebSurfer: Error checking version")

try:
    print(f"RoundRobinGroupChat: {RoundRobinGroupChat.component_version}")
except:
    print("RoundRobinGroupChat: Error checking version")

try:
    print(f"SelectorGroupChat: {SelectorGroupChat.component_version}")
except:
    print("SelectorGroupChat: Error checking version")
