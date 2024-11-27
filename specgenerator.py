from openai import OpenAI
import json
client = OpenAI()

def save_openapi_spec(spec_text):
    file_path = "openapi_spec.yml"
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(spec_text)
        print(f"OpenAPI specification saved to {file_path} successfully.")
        return "OpenAPI specification saved to {file_path} successfully."
    except IOError as e:
        print(f"Error saving OpenAPI specification to {file_path}: {e}")
        return f"Error saving OpenAPI specification to {file_path}: {e}"

tools = [
    {
    "type": "function",
    "function": {
        "name": "save_openapi_spec",
        "description": "Save an OpenAPI specification to a file",
        "parameters": {
        "type": "object",
        "properties": {
            "spec_text": {
            "type": "string",
            "description": "The OpenAPI specification text to be saved to a file"
            }
        },
        "required": ["spec_text"]
        }
    }
    }
    
]

messages=[
        {"role": "system", "content": "You are a helpful assistant who give consistence result based on same input"},
    ]

def generate_openAPI_spec(prompt):
    global messages
    if prompt:messages.append({"role": "user", "content": prompt})
    completion = client.chat.completions.create(
      model="gpt-4o",
      messages=messages,
      tools=tools,
      tool_choice="auto",
      parallel_tool_calls=False,
      temperature=0.0,
    )
    
    messages.append(completion.choices[0].message)
    print(messages)

    if(completion.choices[0].finish_reason=="tool_calls"):
        for tool in completion.choices[0].message.tool_calls:
            if tool.function.name == "save_openapi_spec":
                code = json.loads(tool.function.arguments)
                result = save_openapi_spec(code['spec_text'])
                messages.append({"role": "tool", "content": result, "tool_call_id":tool.id})
                return "tool_call"
    else:
        return completion.choices[0].message.content



    
