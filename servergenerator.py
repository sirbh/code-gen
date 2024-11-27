from openai import OpenAI
import os
import re

client = OpenAI()
import yaml
import json
import utility
import subprocess





def save_json(json_data):
    json_fix = client.chat.completions.create(
                      model="gpt-4o",
                      messages=[
                          {"role": "system", "content": "You are a helpful assistant who give consistence result based on same input"},
                          {"role": "user", "content":f'''fix the following json {json_data} and return only the fixed json no other text or info'''}
                      ],
                      temperature=0.0,
                    )
    json_data = json_fix.choices[0].message.content
    json_data = json.loads(json_data.replace("```json","").replace("```",""))
    utility.save_server_code("express-server", json_data)

    return "code saved"



def call_function_by_name(module, func_name, *args, **kwargs):
    try:
        func = getattr(module, func_name)
        return func(*args, **kwargs)
    except AttributeError:
        print(f"Function '{func_name}' not found in module '{module.__name__}'")
    except Exception as e:
        print(f"An error occurred: {e}")



tools = [
  {
  "type": "function",
  "function": {
    "name": "save_json",
    "description": "Save a JSON string to a file",
    "parameters": {
      "type": "object",
      "properties": {
        "json_data": {
          "type": "string",
          "description": "The JSON object to be saved to a file"
        }
      },
      "required": ["json_data"]
    }
  }
}
]


def generate_server_code(openapi_spec):
  prompt = f"""
  Here is an OpenAPI specification:
  {openapi_spec}
  
  Generate server code based on the OpenAPI specification in NodeJs. Use the following tools:
  1. prisma for database interaction
  2. postgresql as the database
  3. docker for containerization
  4. expressjs for the server

  create docker compose file which setup database and server container.

  Also create env file with proper env variables and readme.md with proper instruction.
  
  This is the folder structure for your reference:

  ├── controllers/
  │   ├── index.js
  │
  ├── routes/
  │   ├── index.js
  │
  ├── prisma/
  │   ├── schema.prisma
  │
  ├── Dockerfile
  ├── readme.md
  ├── docker-compose.yml
  ├── .env
  ├── server.js
  └── package.json
   
  you can use docker compose to setup database and prisma to make database queries
  Name of server service should be "server" and database service should be "database"
  Application should be ready to run
  Generate single json object where key is directory name and value is the code this file should contain. The json should single level only with no nested objects.Save this json to file.
  """
  
  messages=[
      {"role": "system", "content": "You are a helpful assistant who give consistence result based on same input"},
      {"role": "user", "content": prompt}
  ]
  completion = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=tools,
    tool_choice="auto",
    # parallel_tool_calls=True,
    temperature=0.0,
    # response_format={"type": "json_object"}
  )
  # print(completion.choices[0].message)

  # print(type(completion.choices[0].message))


  if completion.choices[0].finish_reason == "tool_calls":
            for tool in completion.choices[0].message.tool_calls:
                if(tool.function.name == "save_json"):
                    json_data = json.loads(tool.function.arguments)["json_data"]
                    save_json(json_data)
                    

  # save_json(completion.choices[0].message.content.replace("```json","").replace("```",""))
  
 