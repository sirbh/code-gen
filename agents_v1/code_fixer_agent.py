import os, getpass
import shutil
from dotenv import load_dotenv

import json

from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI


from typing_extensions import TypedDict
from pydantic import BaseModel, Field

# Load your OpenAI key
load_dotenv(override=True)
def _set_env(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"{var}: ")
_set_env("OPENAI_API_KEY")

class ResponseFormatter(BaseModel):
    """Always use this tool to structure your response to the user."""
    json_str: str = Field(description="A JSON string representing the server code")

class OverallState(TypedDict):
    server_code:str
    errors: str





def save_server_code(directory_name, json_data):

    print("Saving server code...")
    # Ensure the directory path is within the current working directory
    directory_path = os.path.join(os.getcwd(), directory_name)

    # If the directory exists, remove it and all its contents
    if os.path.exists(directory_path):
        shutil.rmtree(directory_path)

    # Create a fresh directory
    os.makedirs(directory_path)

    # Iterate through the dictionary and write files
    for relative_path, content in json_data.items():
        file_path = os.path.join(directory_path, relative_path)

        # Create any necessary subdirectories
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Write the content to the file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)

    print(f"Files created successfully in {directory_path}.")

def dir_to_json(root_dir):
    result = {}
    for foldername, _, filenames in os.walk(root_dir):
        for filename in filenames:
            filepath = os.path.join(foldername, filename)
            # Get relative path like "prisma/schema.prisma"
            relative_path = os.path.relpath(filepath, root_dir)
            # Read file content
            with open(filepath, 'r', encoding='utf-8') as f:
                result[relative_path] = f.read()
    return json.dumps(result, indent=2)

# Example usage
root_directory = "server_code"  




llm = ChatOpenAI(model="gpt-4o", temperature=0)
llm_with_output = llm.with_structured_output(ResponseFormatter)


# 4. Assistant node: calls LLM
def assistant(state: OverallState)-> OverallState:
    """
    This function fixed server code based on the instructions provided.
    """


    prompt = """
You are given a JSON string that represents server code and your job is to fix the server.
your are provided the error make sure to fix the server code based on the errors:


these are the errors:{errors}

server code: {server_code}

return all the server code in a valid JSON string format as provided with fixes done.
only edit the file that is causing the error, do not change any other file.
example output: {{ "json_str": "{{
   key: value,
   key: value
}}" }}
"""

    print(state)

    json_string = dir_to_json(root_directory)
    # Call the LLM with the prompt
    response = llm_with_output.invoke(prompt.format(
        server_code=json_string,
        errors=state.get("errors", "")
    ))

    
    # Update the state with the generated server code
    return {
        "server_code": response.json_str
    }

def json_fixer(state: OverallState) -> OverallState:
    
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

# 5. Graph setup

builder = StateGraph(OverallState)
builder.add_node("assistant", assistant)
builder.add_node("json_fixer", json_fixer)

builder.add_edge(START, "assistant")
builder.add_edge("assistant", "json_fixer")

builder.add_edge("json_fixer", END)

# Compile
graph = builder.compile()

