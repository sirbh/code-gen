import os, getpass
from dotenv import load_dotenv

from langgraph.graph import MessagesState, StateGraph, START
from langgraph.prebuilt import tools_condition, ToolNode
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver

from openapi_spec_validator import validate_spec
from openapi_spec_validator.exceptions import OpenAPISpecValidatorError
import yaml

from pydantic import BaseModel, Field


# Load your OpenAI key
load_dotenv(override=True)
def _set_env(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"{var}: ")
_set_env("OPENAI_API_KEY")



memory = MemorySaver()



class ResponseFormatter(BaseModel):
    """Always use this tool to structure your response to the user."""
    json_str: str = Field(description="A JSON string representing the openapi spec")

# 2. LLM setup with tools
llm = ChatOpenAI(model="gpt-4o", temperature=0)




# JSON fixer agent 
def json_fixer(spec:str) -> str:

    print("Fixing JSON spec...")
    
    prompt = """

    You are given a JSON string that represents server code.
    Your task is to ensure that the JSON string is valid and does not throw an error when passed to the `json.loads` method in Python.

    Here is the JSON string:
    {specification}
    Please ensure that the JSON string is properly formatted and valid.
    """

    llm_with_output = llm.with_structured_output(ResponseFormatter)

    response = llm_with_output.invoke(prompt.format(specification=spec))

    response_json = response.json_str

    return response_json



@tool
def save_openapi_spec(spec: str) -> str:
     
    """Saves the OpenAPI 3.0 spec to a file.
    Args:
        spec (str): The OpenAPI spec string in  JSON format.
    """

    fixed_spec = json_fixer(spec)
    filename = "openapi.json"
    with open(filename, "w") as f:
        f.write(fixed_spec)
    return f"OpenAPI spec saved to {filename}"

@tool
def validate_openapi_spec(spec: str) -> str:
    """Validates an OpenAPI 3.0 spec given as a YAML or JSON string.

    Args:
        spec (str): The OpenAPI spec string in JSON format.
    
    """
    try:
        spec_dict = yaml.safe_load(spec)
        validate_spec(spec_dict)
        return "✅ The OpenAPI spec is valid."
    except OpenAPISpecValidatorError as e:
        return f"❌ Validation failed: {str(e)}"
    except Exception as e:
        return f"⚠️ Error while loading or validating the spec: {str(e)}"



tools = [save_openapi_spec, validate_openapi_spec]
llm_with_tools = llm.bind_tools(tools, parallel_tool_calls=False)



# System message
sys_msg = SystemMessage(content="You are an OpenAPI spec generator who can help user in writing and validating the openAPI specification. Generate OpenAPI 3.0 specs in json format based on the user's request and save it")

# ssistant node: calls LLM
def assistant(state: MessagesState):
    return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}




def create_graph(checkpointer):

     builder = StateGraph(MessagesState)
     builder.add_node("assistant", assistant)
     builder.add_node("tools", ToolNode(tools))
     
     builder.add_edge(START, "assistant")
     builder.add_conditional_edges("assistant", tools_condition)
     builder.add_edge("tools", "assistant")  # optional: loop back to LLM if needed
     
     # Compile
     graph = builder.compile(checkpointer=checkpointer)

     return graph


