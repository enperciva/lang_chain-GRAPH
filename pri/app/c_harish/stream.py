# --------------------------------------------------------------------------------------------
# Este ejercicio muestra como observar la serie de eventos que se ejecutan en determinado grafo
# --------------------------------------------------------------------------------------------
#from langchain_openai import ChatOpenAI
# Libreria del modelo llm
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_community.tools import TavilySearchResults
from typing import TypedDict, Annotated
from langgraph.graph import add_messages, StateGraph, END
from dotenv import load_dotenv
from langgraph.prebuilt import ToolNode
import os
from pprint import pprint

load_dotenv()

# Credenciales de api del llm de google 
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

search_tool = TavilySearchResults(max_results=2)
tools = [search_tool]

llm =  ChatGoogleGenerativeAI (model="gemini-2.0-flash", temperature=0) 

llm_with_tools = llm.bind_tools(tools=tools)

def model(state: AgentState):
    return {
        "messages": [llm_with_tools.invoke(state["messages"])], 
    }

def tools_router(state: AgentState):
    last_message = state["messages"][-1]

    if(hasattr(last_message, "tool_calls") and len(last_message.tool_calls) > 0):
        return "tool_node"
    else: 
        return END
    
print("paso 1111111111111111111111")
tool_node = ToolNode(tools=tools)
print("paso 2222222222222222222")
graph = StateGraph(AgentState)
print("paso 333333333333333333333")
graph.add_node("model", model)
print("paso 4444444444444444444444")
graph.add_node("tool_node", tool_node)
print("paso 55555555555555555555555")
graph.set_entry_point("model")
print("paso 555555555555555555555555")
graph.add_conditional_edges("model", tools_router)
print("paso 666666666666666666666666")
graph.add_edge("tool_node", "model")
print("paso 77777777777777777777777777")
app = graph.compile()
print("paso 8888888888888888888888888")
input = {
    "messages": ["What's the current weather in Bangalore?"]
}
print("paso 99999999999999999999999999")
events = app.stream(input=input, stream_mode="values")
print("paso 10101010101010101010101010")

import json
for event in events: 
    print(event["messages"])
    #print(json.dumps(event, indent=2))  # Imprime los resultados de forma estructurada



"""     input = {
    "messages": ["What's the current weather in Bangalore?"]
}

events = app.stream(input=input, stream_mode="updates")

for event in events: 
    print(event) """


""" input = {
    "messages": ["Hi, how are you?"]
}

events = app.astream_events(input=input, version="v2")

async for event in events: 
    print(event) """


""" input = {
    "messages": ["Hi, how are you?"]
}

events = app.astream_events(input=input, version="v2")

async for event in events: 
    if event["event"] == "on_chat_model_stream":
        print(event["data"]["chunk"].content, end="", flush=True) """