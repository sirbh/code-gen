import json

from agents_v1.spec_generator_agent import graph as spec_generator_agent
from agents_v1.code_generator_agent import graph as code_generator_agent
from agents_v1.code_tester_agent import graph as code_tester_agent


from langchain_core.messages import HumanMessage

from utils.helper import save_server_code




config = {"configurable": {"thread_id": "1"}}
config_code_tester = {"configurable": {"thread_id": "code_tester_agent_run"}}

server_dir = "server_code"


# Start spec generator agent

while True:
    user_input = input("You: ")
    if user_input.lower() in {"exit", "quit"}:
        print("👋 Exiting OpenAPI bot.")
        break

    messages = [HumanMessage(content=user_input)]
    result = spec_generator_agent.invoke({"messages": messages}, config)

    print("\n🔍 Bot:")
    result["messages"][-1].pretty_print()

    print("\n💾 if you have saved the spec in openapi.json file you can move forward for code generation by typing 'exit' or 'quit'")


# Start code generator agent

print("Starting code generation...")

result = code_generator_agent.invoke({
    "server_code": ""
})

save_server_code(server_dir, json.loads(result["server_code"]))



print(f"Server code saved in {server_dir} directory. You can now ask me to run docker compose or ask me list of things I can do.")

# Start code tester agent


while True:
    user_input = input("You: ")
    if user_input.lower() in {"exit", "quit"}:
        print("👋 Exiting code generation bot.")
        break

    messages = [HumanMessage(content=user_input)]
    result = code_tester_agent.invoke({"messages": messages}, config_code_tester)

    print("\n🔍 Bot:")
    result["messages"][-1].pretty_print()






