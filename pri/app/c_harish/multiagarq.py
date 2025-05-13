from dotenv import load_dotenv
import os
from typing import TypedDict, Annotated
from langgraph.graph import add_messages, StateGraph, END
#from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import ToolNode
# Libreria del modelo llm
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


# Credenciales de api del llm de google 
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

# Credenciales de api Tavitys
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")


os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")

# Define the llm 
llm =  ChatGoogleGenerativeAI (model="gemini-2.0-flash", temperature=0) 


# Declara la clase estado
# 'add_messages' añade un mensaje unicial a la conversacion con el llm, asegurandose que la conversacion se inicialice
class ChildState(TypedDict):
    messages: Annotated[list, add_messages]


search_tool = TavilySearchResults(max_results=2)
tools = [search_tool]

#llm = ChatGroq(model="llama-3.1-8b-instant")

llm_with_tools = llm.bind_tools(tools=tools)

def agent(state: ChildState):
    #print("el inicial es : ", state["messages"])
    return {
        "messages": [llm_with_tools.invoke(state["messages"])], 
    }

# El subgrafo que tiene una condicionante, envia el flujo hacia esta funcion
# que a la vez tiene una condicionante que determinara hacia donde seguira el flujo
def tools_router(state: ChildState):
    last_message = state["messages"][-1]

    if(hasattr(last_message, "tool_calls") and len(last_message.tool_calls) > 0):

        return "tool_node"
    else:

        print("me quite ----------------", last_message)
        return END
    
#Aunque tool_node se trata como una variable, internamente se reconoce como un NODO de herramientas
tool_node = ToolNode(tools=tools)

subgraph = StateGraph(ChildState)

subgraph.add_node("agent", agent)
subgraph.add_node("tool_node", tool_node)

#subgraph.add_edge(START, "supervisor")  
subgraph.set_entry_point("agent")

subgraph.add_conditional_edges("agent", tools_router)
subgraph.add_edge("tool_node", "agent")

search_app = subgraph.compile()

#print("invocando a panama")
search_app.invoke({"messages": [HumanMessage(content="How is the weather in Panama?")]})



# Case 1: Shared Schema (Direct Embedding)

from typing import TypedDict, Annotated
from langgraph.graph import add_messages, StateGraph, START, END
from langchain_core.messages import HumanMessage

# Define parent graph with the same schema
class ParentState(TypedDict):
    messages: Annotated[list, add_messages]

# Create parent graph
parent_graph = StateGraph(ParentState)

# Add the subgraph as a node
parent_graph.add_node("search_agent", search_app)

# Connect the flow
parent_graph.add_edge(START, "search_agent")
parent_graph.add_edge("search_agent", END)

# Compile parent graph
parent_app = parent_graph.compile()


print("invocando a Moscu")
# Run the parent graph
result = parent_app.invoke({"messages": [HumanMessage(content="How is the weather in Moscu?")]})
result


from typing import TypedDict, Annotated, Dict
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage

# Define parent graph with different schema
class QueryState(TypedDict):
    query: str
    response: str

# Function to invoke subgraph
def search_agent(state: QueryState) -> Dict:
    # Transform from parent schema to subgraph schema
    subgraph_input = {
        "messages": [HumanMessage(content=state["query"])]
    }
    
    # Invoke the subgraph
    subgraph_result = search_app.invoke(subgraph_input)
    
    # Transform response back to parent schema
    assistant_message = subgraph_result["messages"][-1]
    return {"response": assistant_message.content}

# Create parent graph
parent_graph = StateGraph(QueryState)

# Add transformation node that invokes subgraph
parent_graph.add_node("search_agent", search_agent)

# Connect the flow
parent_graph.add_edge(START, "search_agent")
parent_graph.add_edge("search_agent", END)

# Compile parent graph
parent_app = parent_graph.compile()

print("invocando a Santiago")
# Run the parent graph
result = parent_app.invoke({"query": "How is the weather in Santiago, Republica Dominicana?", "response": ""})
print(result)


