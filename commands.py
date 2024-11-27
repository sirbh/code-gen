import subprocess
import os
import requests
import random
import string
import json


def run_docker_compose(directory_name="express-server", timeout=300):
    """
    Run a Docker Compose command in the specified directory and return combined output and error logs.

    Args:
    - directory_name (str): The name of the directory where the Docker Compose command will be run.
    - timeout (int): The maximum time (in seconds) to wait for the Docker Compose command to complete.

    Returns:
    - str: Combined output and error logs.
    """
    try:
        directory = os.path.join(os.getcwd(), directory_name)

        if not os.path.isdir(directory):
            raise ValueError(f"The directory {directory} does not exist.")

        command = ["docker-compose", "up", "--build", "--force-recreate", "-d"]

        # Start the command
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=directory)

        try:
            # Wait for the process to complete or timeout
            stdout, stderr = process.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            process.kill()
            stdout, stderr = process.communicate()
            return f"Process timed out. Partial logs:\n{stdout}\n{stderr}"

        # Combine stdout and stderr
        logs = stdout + stderr
        return logs

    except Exception as e:
        return f"An error occurred: {e}"


# def run_docker_compose(directory_name="express-server"):
#     """
#     Run a Docker Compose command in the specified directory and return combined output and error logs.

#     Args:
#     - directory_name (str): The name of the directory where the Docker Compose command will be run.

#     Returns:
#     - list: A list of strings containing combined output and error logs.
#     """
#     try:

#         directory = os.path.join(os.getcwd(), directory_name)


#         if not os.path.isdir(directory):
#             raise ValueError(f"The directory {directory} does not exist.")

#         command = ["docker-compose", "up", "--build", "--force-recreate", "-d"]

#         # Start the command
#         process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=directory)

#         logs = []

#         # Read the output line by line
#         while True:
#             output = process.stdout.readline()
#             error = process.stderr.readline()

#             if output:
#                 logs.append(output.strip())
#                 print(output.strip())
#             if error:
#                 logs.append(error.strip())
#                 print(error.strip())

#             # Check if process has terminated
#             if output == '' and error == '' and process.poll() is not None:
#                 break

#         # Read any remaining output and errors
#         remaining_output, remaining_error = process.communicate()
#         if remaining_output:
#             logs.extend(remaining_output.strip().split('\n'))
#         if remaining_error:
#             logs.extend(remaining_error.strip().split('\n'))

#         return "\n".join(logs)

#     except Exception as e:
#         return [f"An error occurred: {e}"]


def get_services_status(directory_name="express-server"):
    try:
        # Ensure the provided directory exists
        directory = os.path.join(os.getcwd(), directory_name)
        if not os.path.isdir(directory):
            raise ValueError(f"The directory {directory} does not exist.")
        
        # Command to get the status of services
        command = ["docker-compose", "ps", "-a"]
        
        # Run the command in the specified directory
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=directory)
        
        # Print output if needed
        return result.stdout
        
    except subprocess.CalledProcessError as e:
        # Handle error
        return f"Error: {e.stderr}"

    except ValueError as ve:
        return f"Error: {ve}"

def get_service_logs(directory_name="express-server",cmd_time="2h"):
    try:
        # Ensure the provided directory exists
        directory = os.path.join(os.getcwd(), directory_name)
        if not os.path.isdir(directory):
            raise ValueError(f"The directory {directory} does not exist.")
        
        # Command to get the logs of a service
        command = ["docker-compose", "logs", "--since", cmd_time]
        
        # Run the command in the specified directory
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=directory)
        
        # Print output if needed
        return result.stdout
        
    except subprocess.CalledProcessError as e:
        # Handle error
        return f"Error: {e.stderr}"

    except ValueError as ve:
        return f"Error: {ve}"


import subprocess

def curl_request(command, timeout=5):
    """
    Makes a curl request to the specified URL with a maximum timeout.

    :param url: The URL to request.
    :param timeout: The maximum time in seconds to wait for the operation.
    :return: The output of the curl command or an error message.
    """
    try:
        # Construct the curl command with timeout
        # command = ["curl", "--max-time", str(timeout), url]
        
        # Run the command and capture the output
        result = subprocess.run(command+" --max-time 5", stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=timeout, shell=True)

        print(command)

        print(result)
        
        # Check if the command was successful
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return f"Error: {result.stderr.strip()}"
    
    except subprocess.TimeoutExpired:
        return f"Error: Request timed out after {timeout} seconds."
    except subprocess.CalledProcessError as e:
        return f"Error running curl command: {e}"


def run_prisma_migrate(directory_name,service_name):
    """
    Run `npx prisma migrate dev` inside a Docker Compose service with a random migration name.

    :param service_name: The name of the service defined in the docker-compose.yml file.
    :return: Output from the command.
    """
    try:

        directory = os.path.join(os.getcwd(), directory_name)
        if not os.path.isdir(directory):
            raise ValueError(f"The directory {directory} does not exist.")
        # Generate a random string for the migration name
        migration_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))

        # Construct the prisma migrate command
        command = f"npx prisma db push"

        # Construct the docker-compose exec command
        docker_compose_command = ['docker-compose', 'exec', service_name] + command.split()

        # Run the command and capture the output
        result = subprocess.run(docker_compose_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=directory)

        # Check if the command was successful
        if result.returncode == 0:
            return result.stdout
        else:
            return f"Error: {result.stderr}"

    except Exception as e:
        return f"Exception occurred: {str(e)}"


def send_api_request(url, params=None, headers=None, request_type='GET'):
    """
    Send an API request.

    Parameters:
    - url (str): The URL of the API endpoint.
    - params (str or dict, optional): The query parameters or JSON body to include in the request.
    - headers (str or dict, optional): The headers to include in the request.
    - request_type (str, optional): The type of request to send ('GET', 'POST', 'PUT', 'DELETE'). Default is 'GET'.

    Returns:
    - Response object or None if the request fails.
    """
    try:
        # Convert params and headers from JSON strings to dictionaries if necessary
        if isinstance(params, str):
            params = json.loads(params)
        if isinstance(headers, str):
            headers = json.loads(headers)
        
        if request_type == 'GET':
            response = requests.get(url, params=params, headers=headers)
        elif request_type == 'POST':
            response = requests.post(url, json=params, headers=headers)
        elif request_type == 'PUT':
            response = requests.put(url, json=params, headers=headers)
        elif request_type == 'DELETE':
            response = requests.delete(url, params=params, headers=headers)
        else:
            raise ValueError("Unsupported request type. Choose from 'GET', 'POST', 'PUT', 'DELETE'.")

        # Check if the request was successful
        response.raise_for_status()  # Raise an exception for HTTP errors

        return response
    except json.JSONDecodeError as e:
        return f"Invalid JSON format: {e}"
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"


