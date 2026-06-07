from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_core.messages import BaseMessage
import sqlite3

load_dotenv()

conn = sqlite3.connect(
    "chatbot.db",
    check_same_thread=False
)

checkpointer = SqliteSaver(conn)

llm = ChatGroq(
    model="llama-3.3-70b-versatile"
)

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def chatbot_node(state: ChatState):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

builder = StateGraph(ChatState)

builder.add_node("chatbot", chatbot_node)

builder.add_edge(START, "chatbot")
builder.add_edge("chatbot", END)

chatbot = builder.compile(
    checkpointer=checkpointer
)