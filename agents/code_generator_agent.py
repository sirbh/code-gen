import os, getpass
from dotenv import load_dotenv

import json

from langgraph.graph import MessagesState, StateGraph, START
from langgraph.prebuilt import tools_condition, ToolNode
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver

from openapi_spec_validator import validate_spec
from openapi_spec_validator.exceptions import OpenAPISpecValidatorError
import yaml

# Load your OpenAI key
load_dotenv()
def _set_env(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"{var}: ")
_set_env("OPENAI_API_KEY")



def read_file_as_string(filepath: str) -> str:
    """Read the entire contents of a file and return as a string."""
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()
    
spec = read_file_as_string("openapi.yaml")
prompt = read_file_as_string("prompts/code_generator_agent_prompt.txt").replace("{{INSERT_OPENAPI_SPEC_HERE}}", spec)


@tool
def save_code(code_json_str: str) -> str:
    """
    Save code represented as a JSON string into files under a directory called 'server_code'.
    """
    base_dir: str = "server_code"
    

    try:
        code_json = json.loads(code_json_str)
        file_count = 0

        def write_files(current_json, current_path):
            nonlocal file_count
            for name, content in current_json.items():
                path = os.path.join(current_path, name)
                if isinstance(content, dict):
                    os.makedirs(path, exist_ok=True)
                    write_files(content, path)
                else:
                    # Fix: if content is a dict (like for package.json), convert to JSON string
                    if name.endswith(".json") and isinstance(content, dict):
                        content = json.dumps(content, indent=2)

                    os.makedirs(os.path.dirname(path), exist_ok=True)
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(str(content))
                    file_count += 1

        if os.path.exists(base_dir):
            return f"⚠️ Directory '{base_dir}' already exists. Files may be overwritten."

        os.makedirs(base_dir)
        write_files(code_json, base_dir)

        return f"✅ Code saved successfully to '{base_dir}/' with {file_count} files."

    except Exception as e:
        return f"❌ Failed to save code: {str(e)}"




tools = [save_code]

# 2. LLM setup with tools
llm = ChatOpenAI(model="gpt-4o", temperature=0)
llm_with_tools = llm.bind_tools(tools, parallel_tool_calls=False)

# 3. System message
sys_msg = SystemMessage(content="You are a senior backend engineer specialized in Node.js, Express.js, Prisma, and Docker.")

# 4. Assistant node: calls LLM
def assistant(state: MessagesState):
    return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}

# 5. Graph setup
builder = StateGraph(MessagesState)
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))
builder.add_edge(START, "assistant")
builder.add_conditional_edges("assistant", tools_condition)
builder.add_edge("tools", "assistant")  # optional: loop back to LLM if needed

# Compile
graph = builder.compile()

messages = [HumanMessage(content=prompt)]
result = graph.invoke({"messages": messages})

print("\n🔍 Bot:")
result["messages"][-1].pretty_print()

# while True:
#     user_input = input("You: ")
#     if user_input.lower() in {"exit", "quit"}:
#         print("👋 Exiting OpenAPI bot.")
#         break

#     messages = [HumanMessage(content=user_input)]
#     result = graph.invoke({"messages": messages}, config)

#     print("\n🔍 Bot:")
#     result["messages"][-1].pretty_print()
