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

    return "code saved as per the instructions" 



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






def fix_server_code(code,instructions):
  prompt = f"""
  Here is the issue and instructions:
  {instructions}

  And Here is the server code that needs to be fixed:
  {code}
  
  Fix the code and return the fixed code in the json format as provided with all the keys and code as given in the code.

  Save the json to the file
  """

  print(prompt)
  
  messages=[
      {"role": "system", "content": "You are a helpful assistant who give consistence result based on same input"},
      {"role": "user", "content": prompt}
  ]

  completion = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=tools,
    tool_choice="auto",
    parallel_tool_calls=False,
    temperature=0.0,
    # response_format={"type": "json_object"}
  )
  print(completion.choices[0].message)

  print(type(completion.choices[0].message))


  if completion.choices[0].finish_reason == "tool_calls":
            for tool in completion.choices[0].message.tool_calls:
                if(tool.function.name == "save_json"):
                    json_data = json.loads(tool.function.arguments)["json_data"]
                    save_json(json_data)

            return "server code fixed and saved successfully"
  else:
    return "unable to fix server code not fixed"
                    

  save_json(completion.choices[0].message.content.replace("```json","").replace("```",""))




  
 