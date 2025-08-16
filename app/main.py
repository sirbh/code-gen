from fastapi import FastAPI, Request, Depends,Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.responses import JSONResponse, Response
from uuid import uuid4

from sqlalchemy.orm import Session
from utils.helper import save_server_code

from agents_v1.spec_generator_agent import create_graph as spec_generator_create_graph
from agents_v1.code_generator_agent import create_graph as code_generator_create_graph
from agents_v1.code_tester_agent import create_graph as code_tester_create_graph

from contextlib import asynccontextmanager
# from .agent_memory.db import init_memory

from langchain.schema import HumanMessage, AIMessage
from langchain_core.messages import ToolMessage
from langgraph.checkpoint.memory import InMemorySaver

import os,json,gzip
from fastapi import Request, HTTPException
import logging
import traceback









@asynccontextmanager
async def lifespan(app: FastAPI):
    
    # store, store_ctx, checkpointer_ctx = await init_memory()
    checkpointer = InMemorySaver()
    # await store.setup()
    # await checkpointer.setup()
    # app.state.store = store
    app.state.checkpointer = checkpointer
    app.state.graph = spec_generator_create_graph(checkpointer)
    app.state.server_generator_graph = code_generator_create_graph(checkpointer)
    app.state.tester_graph = code_tester_create_graph(checkpointer)
    app.state.server_dir = "server_code"
    app.state.spec_thread = str(uuid4())
    app.state.server_thread = str(uuid4())
    app.state.tester_thread = str(uuid4())

    yield

    # await store_ctx.__aexit__(None, None, None)
    # await checkpointer_ctx.__aexit__(None, None, None)


app = FastAPI(lifespan=lifespan)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
async def health_check():



    return {"status": "ok", "message": "API is running smoothly."}


@app.get("/api/reset")
async def reset_chat(request: Request):
    app.state.spec_thread = str(uuid4())
    app.state.server_thread = str(uuid4())
    app.state.tester_thread = str(uuid4())
    return {"status": "ok", "message": "Chat reset successfully."}


@app.get("/api/chat")
def get_chat_messages(request: Request):


    spec_graph = app.state.graph
    server_graph = app.state.server_generator_graph
    tester_graph = app.state.tester_graph

    
    thread_spec = {
        "configurable": {
            "thread_id": app.state.spec_thread,
        }
    }

    thread_server = {
        "configurable": {
            "thread_id": app.state.server_thread,
        }
    }

    thread_tester = {
        "configurable": {
            "thread_id": app.state.tester_thread,
        }
    }

    state_spec = spec_graph.get_state(thread_spec)
    state_server = server_graph.get_state(thread_server)
    state_tester = tester_graph.get_state(thread_tester)

    messages = []

    if "messages" in state_spec.values:
        msgs = state_spec.values['messages']
        for msg in msgs:
            if isinstance(msg, HumanMessage):
                messages.append({
                    'role': 'user',
                    'content': msg.content
                })
            elif isinstance(msg, AIMessage):
                # finish_reason = msg.response_metadata.get('finish_reason')
                # if finish_reason == 'stop':
                    messages.append({
                        'role': 'ai',
                        'content': msg.content
                    })

    if "custom_message" in state_server.values:
        msg = state_server.values['custom_message']
        messages.append({
            'role': 'ai',
            'content': msg
        })

    if "messages" in state_tester.values:
        msgs = state_tester.values['messages']
        for msg in msgs:
            if isinstance(msg, HumanMessage):
                messages.append({
                    'ai': 'user',
                    'content': msg.content
                })
            elif isinstance(msg, AIMessage):
                messages.append({
                    'ai': 'user',
                    'content': msg.content
                })  

    response_data = {
        "messages": messages
    }

    # Compress the response
    json_data = json.dumps(response_data).encode("utf-8")
    compressed_data = gzip.compress(json_data)

    return Response(
        content=compressed_data,
        media_type="application/json",
        headers={"Content-Encoding": "gzip"}
    )


@app.post("/api/chat")
async def chat_endpoint(
    request: Request,
    body: dict = Body(...),
):

    config = {
        "configurable": {
            "thread_id": app.state.spec_thread,
        }
    }
   
    message = body.get("message", "")
    graph = app.state.graph


    async def event_generator():
        async for event in graph.astream_events(
            {"messages": [HumanMessage(content=message)]},
            config=config,
            version="v2",
        ):
            if event["event"] == "on_chat_model_stream" and event['metadata'].get('langgraph_node', '') == "assistant":
                data = event["data"]
                yield json.dumps({
                    "type": "ai",
                    "content": data["chunk"].content
                }) + "\n"

        
    return StreamingResponse(event_generator(), media_type="text/event-stream")



@app.post("/api/generate-server-code")
async def generate_server_code_endpoint(
    request: Request,
):

    graph = app.state.server_generator_graph
    config = {
            "configurable": {
                "thread_id": app.state.server_thread,
            }
        }

    async def event_generator():
        async for event in graph.astream_events(
            {"server_code": ""},
            config=config,
            version="v2",
        ):
            if event["event"] == "on_chat_model_stream" and event['metadata'].get('langgraph_node', '') == "assistant":
                data = event["data"]
                yield json.dumps({
                    "type": "ai",
                    "content": data["chunk"].content
                }) + "\n"

        st = await graph.aget_state(config=config)


        save_server_code(app.state.server_dir, json.loads(st.values.get("server_code", "")))
        yield json.dumps({
            "type": "ai",
            "content": "Server code generated successfully."
        }) + "\n"

        await graph.aupdate_state(config,{"custom_message": "Server code generated successfully."})

    return StreamingResponse(event_generator(), media_type="text/event-stream") 


@app.post("/api/test-code")
async def chat_endpoint(
    request: Request,
    body: dict = Body(...),
):

    config = {
        "configurable": {
            "thread_id": app.state.tester_thread,
        }
    }
   
    message = body.get("message", "")
    graph = app.state.tester_graph


    async def event_generator():
        async for event in graph.astream_events(
            {"messages": [HumanMessage(content=message)]},
            config=config,
            version="v2",
        ):
            if event["event"] == "on_chat_model_stream" and event['metadata'].get('langgraph_node', '') == "assistant":
                data = event["data"]
                yield json.dumps({
                    "type": "ai",
                    "content": data["chunk"].content
                }) + "\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


            








