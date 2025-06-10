import os, getpass
from dotenv import load_dotenv

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

config = {"configurable": {"thread_id": "1"}}
memory = MemorySaver()

# 1. TOOL: Save the OpenAPI spec to a file
@tool
def save_openapi_spec(spec: str, filename: str = "openapi.yaml") -> str:
    """Save OpenAPI specification string to a file"""
    with open(filename, "w") as f:
        f.write(spec)
    return f"OpenAPI spec saved to {filename}"

@tool
def validate_openapi_spec(spec: str) -> str:
    """Validates an OpenAPI 3.0 spec given as a YAML or JSON string."""
    try:
        spec_dict = yaml.safe_load(spec)
        validate_spec(spec_dict)
        return "✅ The OpenAPI spec is valid."
    except OpenAPISpecValidatorError as e:
        return f"❌ Validation failed: {str(e)}"
    except Exception as e:
        return f"⚠️ Error while loading or validating the spec: {str(e)}"



tools = [save_openapi_spec, validate_openapi_spec]

# 2. LLM setup with tools
llm = ChatOpenAI(model="gpt-4o", temperature=0)
llm_with_tools = llm.bind_tools(tools, parallel_tool_calls=False)

# 3. System message
sys_msg = SystemMessage(content="You are an OpenAPI spec generator. Generate OpenAPI 3.0 specs based on the user's request.")

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
graph = builder.compile(checkpointer=memory)


while True:
    user_input = input("You: ")
    if user_input.lower() in {"exit", "quit"}:
        print("👋 Exiting OpenAPI bot.")
        break

    messages = [HumanMessage(content=user_input)]
    result = graph.invoke({"messages": messages}, config)

    print("\n🔍 Bot:")
    result["messages"][-1].pretty_print()
