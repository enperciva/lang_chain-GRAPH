#===================================================================================
# El siguiente ejercicio se trata de agente de herramientas langgraph
#===================================================================================


# Librerias del ambiente de entorno 
import os
import warnings
warnings.filterwarnings("ignore")
from dotenv import load_dotenv, find_dotenv 

# Librerias de mensajes del chat o prompttemplate
from langgraph.graph import MessagesState 
from langchain_core.messages import SystemMessage 

# Librerias que gestionan el estado y el edge del grafo
from langgraph.graph import StateGraph, START, END 

# Libreria del modelo llm
from langchain_google_genai import ChatGoogleGenerativeAI

# Permite crear un nodo en un gráfico (graph) de LangGraph
from langgraph.prebuilt import ToolNode 

# Libreria que gestiona las condicionales de las adge del grafo
from langgraph.prebuilt import tools_condition 

# Librerias para hacer requests de sitios web
import requests

load_dotenv()

# Credenciales de api del llm de google 
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

class State (MessagesState):
    messmeme: str 


#Define the tools 
def multiply(a: int, b: int) -> int: 
    """ Multiplies a and b. """
    return a * b 
    
def add(a: int, b: int) -> int: 
    """ Adds a and b. """ 
    return a + b

def get_categories() -> str:
    """ Adds a and b. """ 
    #Get the categories of the products.""" 
    response = requests.get("https://api.escuelajs.co/api/v1/categories") 
    categories = response.json() 
    category_names = [category ["name"] for category in categories] 
    return ", ".join(category_names) 


# Define the llm 
llm =  ChatGoogleGenerativeAI (model="gemini-2.0-flash", temperature=0) 

# parallel_tool_calls determina si las herramientas se ejecutaran en paralelo o de modo secuencial
#llm = llm.bind_tools(tools, parallel_tool_calls=False) 

# tools es una caja de herramientas declarada abajo en el grafo "tools" (builder.add_node("tools", ToolNode (tools)) )
tools = [multiply, add, get_categories] 

# Vinculo las herramientas al llm
llm = llm.bind_tools(tools) 


""" def tools_condition(state: State) -> bool:
    # Verificar si la condición para usar las herramientas es verdadera
    if state.get("action_needed") == "activate_tools":
        return True
    return False
 """

# Nodo
def assistant(state: State) -> State: 
    system_message = SystemMessage(content="Eres un experto en matemáticas. Tambien tienes conocimientos de categorias de productos")
    #State.messages = "hola como estas"
    return {"messages": [llm.invoke([system_message] + state["messages"])]}


# Define the graph 
builder = StateGraph(MessagesState)

builder.add_node('assistant', assistant) 
builder.add_node("tools", ToolNode (tools)) 

# Define las etapas de ejecucion
builder.add_edge (START, 'assistant') 

# Define una condicion de ejecucion
builder.add_conditional_edges("assistant", tools_condition) 

""" builder.add_conditional_edges(
    "assistant",
    condition=tools_condition,
    path_map={
        True: "tools",   # Si la condición devuelve True → ir a tools
        False: END       # Si devuelve False → terminar
    }
 """

builder.add_edge("tools", "assistant") 

builder.add_edge("assistant", END) 

graph = builder.compile() 

