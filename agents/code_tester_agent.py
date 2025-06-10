import os, getpass
import subprocess

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

config = {"configurable": {"thread_id": "code_tester_agent_1"}}
memory = MemorySaver()

@tool
def run_docker_compose_up() -> str:
    """
    Runs `docker-compose up -d`.

    Returns:
        Message indicating whether the containers were started successfully or any errors.
    """
    try:
        compose_path = "server_code/docker-compose.yml"
        abs_path = os.path.abspath(compose_path)
        dir_path = os.path.dirname(abs_path)

        print(f"📂 Running docker-compose in directory: {dir_path}")
        command = ["docker-compose", "-f", abs_path, "up", "-d"]

        result = subprocess.run(
            command,
            cwd=dir_path,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return f"❌ Failed to start Docker containers:\n{result.stderr.strip()}"

        return f"✅ Docker containers started successfully:\n{result.stdout.strip()}"

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
        compose_path = "server_code/docker-compose.yml"
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
    

# output = run_docker_compose_up()
# print(output)

# logs = get_all_docker_logs()
# print(logs)

def read_file_as_string(filepath: str) -> str:
    """Read the entire contents of a file and return as a string."""
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()
    
# spec = read_file_as_string("product_service_openapi.yaml")
# prompt = read_file_as_string("code_generator_agent_prompt.txt").replace("{{INSERT_OPENAPI_SPEC_HERE}}", spec)




tools = [run_docker_compose_up, get_all_docker_logs]

# 2. LLM setup with tools
llm = ChatOpenAI(model="gpt-4o", temperature=0)
llm_with_tools = llm.bind_tools(tools, parallel_tool_calls=False)

# 3. System message
sys_msg = SystemMessage(content="You run docker containers for a Node.js backend service when user asks. You can start the containers and fetch logs from them. You are an expert in Docker and Debugging Node.js backend code.")

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

# messages = [HumanMessage(content=prompt)]
# result = graph.invoke({"messages": messages})

# print("\n🔍 Bot:")
# result["messages"][-1].pretty_print()

while True:
    user_input = input("You: ")
    if user_input.lower() in {"exit", "quit"}:
        print("👋 Exiting OpenAPI bot.")
        break

    messages = [HumanMessage(content=user_input)]
    result = graph.invoke({"messages": messages}, config)

    print("\n🔍 Bot:")
    result["messages"][-1].pretty_print()
