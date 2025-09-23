from typing import TypedDict
from typing_extensions import Annotated
from langchain_openai import ChatOpenAI
from langgraph.graph import END ,START
from langgraph.graph.state import StateGraph
from langgraph.graph.message import add_messages
from  langgraph.prebuilt import ToolNode
from langchain_core.tools import tool
from langchain_core.messages import BaseMessage
from langchain_groq import ChatGroq


import os 
from dotenv import load_dotenv
load_dotenv()

groq_key = os.getenv("GROQ_API_KEY")
langchain_key = os.getenv("LANGCHAIN_API_KEY")

if groq_key:
    os.environ["GROQ_API_KEY"] = groq_key
else:
    raise RuntimeError("GROQ_API_KEY not found in environment (check your .env path).")

if langchain_key:
    os.environ["LANGCHAIN_API_KEY"] = langchain_key

###
class State(TypedDict):
    messages:Annotated[list[BaseMessage],add_messages]
 
llm=ChatGroq(model="llama-3.1-8b-instant")

def make_default_graph():
    graph_workflow=StateGraph(State)

    def call_model(state):
        return{"messages":[llm.invoke(state["messages"])]}
    
    graph_workflow.add_node("agent",call_model)
    graph_workflow.add_edge(START,"agent")
    graph_workflow.add_edge("agent",END)
   

    agent=graph_workflow.compile()
    return agent
agent= make_default_graph()