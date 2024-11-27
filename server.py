from flask import Flask, request,jsonify, make_response
from flask_cors import CORS
import specgenerator
import servergenerator
import utility
import commands
import json
import datetime
import servercodefixer

from openai import OpenAI
client = OpenAI()




# Create a Flask application instance
app = Flask(__name__)

# Enable CORS
CORS(app)

tester_messages = []
cmd_run_time = "1h"

tools = [
    {
        "type": "function",
        "function": {
            "name": "run_docker_compose",
            "description": "Run a Docker Compose return combined output and error logs.",
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_services_status",
            "description": "Get the status of Docker Compose services.",
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_service_logs",
            "description": "Get logs of Docker Compose services.",
        }
    },
    # {
    #     "type": "function",
    #     "function": {
    #         "name": "curl_request",
    #         "description": "Makes a curl request",
    #         "parameters": {
    #             "type": "object",
    #             "properties": {
    #                 "command": {
    #                     "type": "string",
    #                     "description": "The curl command to be executed."
    #                 }
    #             },
    #             "required": ["command"]
    #         }
    #     }
    # },

     {
  "type": "function",
  "function": {
    "name": "send_api_request",
    "description": "Send an HTTP request to a specified API endpoint.",
    "parameters": {
      "type": "object",
      "properties": {
        "url": {
          "type": "string",
          "description": "The URL of the API endpoint."
        },
        "params": {
          "type": "string",
          "description": "The query parameters or JSON body to include in the request, as a JSON string."
        },
        "headers": {
          "type": "string",
          "description": "The headers to include in the request, as a JSON string."
        },
        "request_type": {
          "type": "string",
          "description": "The type of HTTP request to send (e.g., 'GET', 'POST', 'PUT', 'DELETE'). Default is 'GET'.",
          "enum": ["GET", "POST", "PUT", "DELETE"],
          "default": "GET"
        }
      },
      "required": ["url"]
    }
  }
},
    {
        "type": "function",
        "function": {
            "name": "fix_code",
            "description": "Fix and update the server code.",
            "parameters": {
                "type": "object",
                "properties": {
                    "instructions": {
                        "type": "string",
                        "description": "Clear reason for update and  list of instruction of what needed to be done to fix the code and how code should be updated"
                    }
                },
                "required": ["json_data"]
            }
        }
    },

]


# Define a route for the GET request with parameters
@app.route('/spec', methods=['GET'])
def spec():
    # Get the 'name' parameter from the URL query string
    message = request.args.get('message', 'default')
    # resp = specgenerator.generate_openAPI_spec(message)

    try:
        resp = specgenerator.generate_openAPI_spec(message)
    except Exception as e:
        print(e)
        return str(e)

    if resp == "tool_call":
        return "Spec have been save successfully."
    else:
        return resp

@app.route('/generate', methods=['GET'])
def servergen():

    with open("openapi_spec.yml", "r") as file:
        openapi_spec = file.read()
    
    try:
        servergenerator.generate_server_code(openapi_spec)
        code = utility.directory_to_json("express-server")
        prompt = f"""
    Here is openAPI spec {openapi_spec}
    And here is the server code in json format 
    {code}
    Also providing you the helper function that you can call.
    User can also ask you to send request to the server.
    """  
        global tester_messages
        tester_messages = []
        tester_messages.append({
            "role": "system",
            "content": prompt
        })
        return make_response(jsonify({"message": "Server code generated successfully!"}), 200)
    except Exception as e:
        print(e)
        return make_response(jsonify({"error": str(e)}), 500)





@app.route('/tester', methods=['GET'])
def server_tester():
    message = request.args.get('message', 'default')
    # print(message)

    global tester_messages
    tester_messages.append({
        "role": "user",
        "content": message
    })
    # print(tester_messages)

    # return make_response(jsonify({"message": "Server code generated successfully!"}), 200)

    completion = client.chat.completions.create(
      model="gpt-4o",
      messages=tester_messages,
      tools=tools,
      tool_choice="auto",
      parallel_tool_calls=False,
      temperature=0.0,
      
    )

    if completion.choices[0].finish_reason == "tool_calls":
        tester_messages.append(completion.choices[0].message)
        utility.append_json_to_file(completion.choices[0].message.to_json())
        for tool in completion.choices[0].message.tool_calls:
            if(tool.function.name == "fix_code"):
                params = json.loads(tool.function.arguments)
                print(params)
                # result = servergenerator.save_json(code['instructions']) Add new LLM agenet that takes instruction update server code 
                result = servercodefixer.fix_server_code(utility.directory_to_json("express-server"),params['instructions'])
                commands.run_docker_compose()
                op = commands.run_prisma_migrate("express-server","server")
                print(op)
                print(result)
                tester_messages.append({
                    "role": "tool",
                    "content": result,
                    "tool_call_id": tool.id
                })

                completion = client.chat.completions.create(
                    model="gpt-4o",
                    messages=tester_messages,
                )

                return make_response(jsonify({"message": completion.choices[0].message.content}), 200)
            
            elif(tool.function.name == "run_docker_compose"):
                # cmd_run_time = datetime.datetime.now().isoformat()
                result = commands.run_docker_compose()
                op = commands.run_prisma_migrate("express-server","server")
                print(op)
                tester_messages.append({
                    "role": "tool",
                    "content": str(result),
                    "tool_call_id": tool.id
                })

                completion = client.chat.completions.create(
                    model="gpt-4o",
                    messages=tester_messages,
                )


                return make_response(jsonify({"message": completion.choices[0].message.content}), 200)
            
            elif(tool.function.name == "get_services_status"):
                result = commands.get_services_status()
                tester_messages.append({
                    "role": "tool",
                    "content": str(result),
                    "tool_call_id": tool.id
                })

                completion = client.chat.completions.create(
                    model="gpt-4o",
                    messages=tester_messages,
                )

                return make_response(jsonify({"message": completion.choices[0].message.content}), 200)

            elif(tool.function.name == "get_service_logs"):
                result = commands.get_service_logs()
                tester_messages.append({
                    "role": "tool",
                    "content": str(result),
                    "tool_call_id": tool.id
                })

                completion = client.chat.completions.create(
                    model="gpt-4o",
                    messages=tester_messages,
                )

                

                return make_response(jsonify({"message": completion.choices[0].message.content}), 200)

            elif(tool.function.name == "send_api_request"):
                # cmd_run_time = datetime.datetime.now().isoformat()
                code = json.loads(tool.function.arguments)
                # result = commands.curl_request(code['command'])
                url = code.get('url')
                params = code.get('params', None)
                headers = code.get('headers', None)
                request_type = code.get('request_type', 'GET')

                print(code)
                result = commands.send_api_request(url, params, headers, request_type)
                print(result)
                tester_messages.append({
                    "role": "tool",
                    "content": str(result),
                    "tool_call_id": tool.id
                })

                completion = client.chat.completions.create(
                    model="gpt-4o",
                    messages=tester_messages
                )

                return make_response(jsonify({"message": completion.choices[0].message.content}), 200)
            
        

    else:

        return make_response(jsonify({"message": completion.choices[0].message.content}), 200)
                
                
    


    



# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)