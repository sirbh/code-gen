import os, getpass
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing_extensions import TypedDict

import json

from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import tools_condition, ToolNode
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver




# Load your OpenAI key
load_dotenv(override=True)
def _set_env(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"{var}: ")
_set_env("OPENAI_API_KEY")

class ResponseFormatter(BaseModel):
    """Always use this tool to structure your response to the user."""
    json_str: str = Field(description="A JSON string representing the server code")

class OverallState(MessagesState):
    server_code:str
    custom_message:str





def read_file_as_string(filepath: str) -> str:
    """Read the entire contents of a file and return as a string."""
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

spec_file = "openapi.json"





@tool
def save_code(code_json_str: str) -> str:
    """
    Save code represented as a JSON string into files under a directory called 'server_code'.
    """
    base_dir: str = "server_code"

    try:
        code_data = json.loads(code_json_str)
        return "json loaded successfully and server code saved successfully"
    except json.JSONDecodeError as e:
        return "problem decoding JSON, please ask the user to fix it"

    




tools = [save_code]

# 2. LLM setup with tools
llm = ChatOpenAI(model="gpt-4o", temperature=0)
llm_with_output = llm.with_structured_output(ResponseFormatter)

# 3. System message
sys_msg = SystemMessage(content="You are a senior backend engineer specialized in Node.js, Express.js, Prisma, and Docker.")

# 4. Assistant node: calls LLM
def assistant(state: OverallState)-> OverallState:
    """
    This function generates server code based on the OpenAPI spec provided in the state.
    """
    
    print("Generating server code...")

    spec = read_file_as_string(spec_file)
    prompt = read_file_as_string("prompts/code_generator_agent_prompt.txt").replace("{{INSERT_OPENAPI_SPEC_HERE}}", spec)
    
    # Call the LLM with the prompt
    response = llm_with_output.invoke(prompt)

    
    # Update the state with the generated server code
    return {
        "server_code": response.json_str
    }

def json_fixer(state: OverallState) -> OverallState:

    print("Validating JSON...")
    
    prompt = """

    You are given a JSON string that represents server code.
    Your task is to ensure that the JSON string is valid and does not throw an error when passed to the `json.loads` method in Python.

    Here is the JSON string:
    {server_code}
    Please ensure that the JSON string is properly formatted and valid.
    """

    response = llm_with_output.invoke(prompt.format(server_code=state["server_code"]))

    return {
        "server_code": response.json_str
    }


def create_graph(checkpointer):

    builder = StateGraph(OverallState)
    
    # 3. Add nodes
    builder.add_node("assistant", assistant)
    builder.add_node("json_fixer", json_fixer)

    # 4. Add edges
    builder.add_edge(START, "assistant")
    builder.add_edge("assistant", "json_fixer")
    builder.add_edge("json_fixer", END)

    # 5. Compile the graph
    graph = builder.compile(checkpointer=checkpointer)

    return graph




