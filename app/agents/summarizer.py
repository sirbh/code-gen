from langgraph.graph import StateGraph, MessagesState, START, END
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from app.store.data import get_vector_store
from langchain.tools.retriever import create_retriever_tool
from dotenv import load_dotenv
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode, tools_condition
from typing import List


from langchain.schema import HumanMessage, SystemMessage
from langgraph.checkpoint.memory import InMemorySaver

from langgraph.types import Command, interrupt

load_dotenv(override=True)

# LangChain chat model
llm = ChatOpenAI(model="gpt-4o", temperature=0)


class ResponseFormatter(BaseModel):
    """Always use this tool to structure your response to the user."""
    chat_name: str = Field(description="The name of the chat, based on the user's input.")


# Graph definition
def call_model(state: MessagesState):
    system_instruction = SystemMessage(
        content=(
            "You can summarize chat summary in max 2 words"
        )
    )

    messages = [system_instruction] + state["messages"]
    response = llm.invoke(messages)
    return {"messages": response}


def create_graph():
    builder = StateGraph(MessagesState)
    builder.add_node("assistant", call_model)

    builder.add_edge(START, "assistant")
    builder.add_edge("assistant", END)

    return builder.compile()


