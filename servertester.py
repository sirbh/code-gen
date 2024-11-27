import subprocess
import re
import os
import json
from openai import OpenAI

client = OpenAI()


def save_json(json_data):
    # with open('json_Data.py', 'w') as file:
    #     file.write("json="+tools)
    # return {"message": "Code saved to tools.py"}
    json_data = json.loads(json_data)
    utility.save_server_code("express-server", json_data)

def run_docker_compose(directory_name="express-server"):

    directory_path = os.path.join(os.getcwd(), directory_name)
    
    try:
        # Run the docker-compose command
        result = subprocess.run(
            ['docker-compose', 'up', '-d', '--build'],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=directory_path
        )
        
        # Capture and decode the output
        stdout = result.stdout.decode('utf-8')
        stderr = result.stderr.decode('utf-8')
        
        return stdout, stderr
    except subprocess.CalledProcessError as e:
        # Handle errors in the subprocess execution
        return e.stdout.decode('utf-8'), e.stderr.decode('utf-8')



def check_docker_compose_status(directory):
    try:
        # Run the docker-compose ps command in the specified directory
        result = subprocess.run(
            ['docker-compose', 'ps'],
            cwd=directory,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True  # Ensure output is returned as text (Python 3.7+)
        )
        
        # Capture and print the output
        
        # Return None as we're printing directly
        return result.stdout
    except subprocess.CalledProcessError as e:
        # Handle errors in the subprocess execution
        print("Error:", e.stderr)
        return e.stderr





def get_docker_compose_logs(directory_name="express-server"):

    directory_path = os.path.join(os.getcwd(), directory_name)

    try:
        # Run the docker-compose logs command
        result = subprocess.run(
            ['docker-compose', 'logs'],
            cwd=directory_path,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Capture and decode the output
        stdout = result.stdout.decode('utf-8')
        stderr = result.stderr.decode('utf-8')
        
        return stdout, stderr
    except subprocess.CalledProcessError as e:
        # Handle errors in the subprocess execution
        return e.stdout.decode('utf-8'), e.stderr.decode('utf-8')

def run_curl_command(curl_command):
    try:
        # Run the curl command
        result = subprocess.run(
            curl_command,
            shell=True,  # Allows to pass the command as a single string
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Capture and decode the output
        stdout = result.stdout.decode('utf-8')
        stderr = result.stderr.decode('utf-8')
        
        print("Standard Output:\n", stdout)
        return stdout
        if stderr:
            print("Standard Error:\n", stderr)
    except subprocess.CalledProcessError as e:
        # Handle errors in the subprocess execution
        print("An error occurred while running the curl command.")
        print("Standard Output:\n", e.stdout.decode('utf-8'))
        print("Standard Error:\n", e.stderr.decode('utf-8'))
        return e.stdout.decode('utf-8')

tools = [
    {
        "type": "function",
        "function": {
            "name": "run_docker_compose",
            "description": "Run docker-compose up -d --build",
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_docker_compose_status",
            "description": "Check the status of containers defined in a Docker Compose file.",
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_docker_compose_logs",
            "description": "Fetch the logs of containers defined in a Docker Compose file.",
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_curl_command",
            "description": "Run a curl command and print its output.The curl command to be executed should have max timeout of 3 seconds.",
            "parameters": {
                "type": "object",
                "properties": {
                    "curl_command": {
                        "type": "string",
                        "description": "The curl command to be executed with max timeout of 3 seconds."
                    }
                },
                "required": ["curl_command"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_json",
            "description": "Update server code with the provided JSON data.",
            "parameters": {
                "type": "object",
                "properties": {
                    "json_data": {
                        "type": "string",
                        "description": "The JSON object of the server code to be updated."
                    }
                },
                "required": ["json_data"]
            }
        }
    }
]



def run_server_test(messages):

    completion = client.chat.completions.create(
      model="gpt-4o",
      messages=messages,
      tools=tools,
      tool_choice="auto",
      parallel_tool_calls=True,
      temperature=0.0,
      
    )

    return completion
        



