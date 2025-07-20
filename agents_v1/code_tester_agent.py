import os, getpass
import subprocess

from dotenv import load_dotenv

import json

from langgraph.graph import MessagesState, StateGraph, START
from langgraph.prebuilt import tools_condition, ToolNode
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from langchain_core.tools import tool

from langgraph.checkpoint.memory import MemorySaver

from agents_v1.code_fixer_agent import graph as fixer_graph

from utils.helper import save_server_code


# Load your OpenAI key
load_dotenv(override=True)
def _set_env(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"{var}: ")
_set_env("OPENAI_API_KEY")

load_dotenv(override=True)


memory = MemorySaver()           



compose_path = "server_code/docker-compose.yml"
server_code_path = "server_code"
specfication_path = "openapi.json"



@tool
def run_docker_compose_up() -> str:
    """
    Runs `docker-compose up -d --build --force-recreate` and returns combined logs.
    """
    try:
        abs_path = os.path.abspath(compose_path)
        dir_path = os.path.dirname(abs_path)

        print(f"📂 Running docker-compose in directory: {dir_path}")
        command = ["docker-compose", "-f", abs_path, "up", "--build", "--force-recreate", "-d"]

        result = subprocess.run(
            command,
            cwd=dir_path,
            capture_output=True,
            text=True
        )

        output = (
            f"STDOUT:\n{result.stdout.strip()}\n\n"
            f"STDERR:\n{result.stderr.strip()}"
        )

        if result.returncode != 0:
            return f"❌ Failed to start Docker containers:\n{output}"

        return f"✅ Docker containers started successfully:\n{output}"

    except FileNotFoundError:
        return "❌ docker-compose command not found. Make sure Docker is installed and in PATH."
    except Exception as e:
        return f"❌ Error while running docker-compose: {str(e)}"

@tool
def get_all_docker_logs() -> str:
    """
    Fetch logs from all running Docker containers using docker-compose logs.

    The docker-compose.yml is assumed to be located at: server_code/docker-compose.yml

    Returns:
        Logs from all services as a string or an error message.
    """
    try:
        abs_path = os.path.abspath(compose_path)
        dir_path = os.path.dirname(abs_path)

        print(f"📂 Fetching logs from: {abs_path}")
        command = ["docker-compose", "-f", abs_path, "logs", "--no-color"]

        result = subprocess.run(
            command,
            cwd=dir_path,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return f"❌ Failed to get logs:\n{result.stderr.strip()}"

        logs = result.stdout.strip()
        return f"📜 All service logs:\n{logs if logs else '[No logs available]'}"

    except FileNotFoundError:
        return "❌ docker-compose not found. Make sure Docker is installed and in PATH."
    except Exception as e:
        return f"❌ Error while getting logs: {str(e)}"
    
@tool
def fix_server_code(errors:str) -> str:
    """
    Fixes the server code based on the provided instructions.

    Args:
        instructions (str): Instructions for fixing the server code.
        errors (str): Exact errors that are causing the issue.

    Returns:
        A message indicating whether the code was fixed successfully or any errors.
    """
    # Load the existing server code from the directory

    try:
        # Convert the directory structure to JSON
        json_string = fixer_graph.invoke({
            "server_code": "",
            "errors": errors
        })

        print(json_string)
        
        # Print or save the JSON string
        save_server_code(server_code_path, json.loads(json_string["server_code"]))
        
        return "Server code fixed successfully."
    except Exception as e:
        return f"Error while fixing server code: {str(e)}"
    

import requests
from typing import Optional, Dict, Any

@tool
def make_http_request(
    endpoint: str = "/",
    method: str = "GET",
    data: Optional[Any] = None,
    params: Optional[Dict[str, Any]] = None,
    port: int = 8000,
    headers: Optional[Dict[str, str]] = None,
    timeout: int = 5
) -> str:
    """
    Makes a local HTTP request to the server running on localhost.

    Args:
        endpoint (str): The endpoint to request.
        method (str): The HTTP method to use (GET, POST, etc.).
        data (dict): Data to send in the request body (for POST/PUT).
        params (dict): Query parameters to include in the request.
        port (int): The port on which the server is running.
        headers (dict): Additional headers to include in the request.
        timeout (int): Timeout for the request in seconds.

    Returns:
        str: The response from the server.
    """
    url = f"http://localhost:{port}{endpoint}"

    try:
        response = requests.request(
            method=method.upper(),
            url=url,
            params=params,
            json=data,
            headers=headers,
            timeout=timeout
        )
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Request failed: {str(e)}"




def read_file_as_string(filepath: str) -> str:
    """Read the entire contents of a file and return as a string."""
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()
    





tools = [run_docker_compose_up, get_all_docker_logs, fix_server_code, make_http_request]


llm = ChatOpenAI(model="gpt-4o", temperature=0)
llm_with_tools = llm.bind_tools(tools, parallel_tool_calls=False)



def assistant(state: MessagesState):
    sys_prompt = """
You run docker containers for a Node.js backend service when user asks. You can start the containers and fetch logs from them. You are an expert in Docker and Debugging Node.js backend code.
this is the server code docker compose file for the services:
{docker_compose_file}
This is the openAPI specification for the server code:
{specification}

"""
    sys_msg = SystemMessage(content=sys_prompt.format(docker_compose_file=read_file_as_string(compose_path),
                                                      specification=read_file_as_string(specfication_path)))
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
