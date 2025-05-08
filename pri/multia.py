#===================================================================================
# El siguiente ejercicio se trata de multiagentes
#===================================================================================
import os
import warnings
warnings.filterwarnings("ignore")
from dotenv import load_dotenv, find_dotenv 

# Declara modelo llm
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

# librerias que manejan los grafos o el enjambre
from langgraph.graph import StateGraph, END
from dataclasses import dataclass

load_dotenv()

# Credenciales de api del llm de google 
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

# Definir el estado del enjambre como un dataclass
@dataclass
class SwarmState:
    pregunta: str
    investigacion: str = ""
    analisis: str = ""
    respuesta_final: str = ""

# Declara modelo llm
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.5)

# Crear agentes con diferentes instrucciones (roles)
def investigador_agent(state: SwarmState):
    pregunta = state.pregunta
    respuesta = llm.invoke(f"Eres un investigador. Busca información relevante sobre: {pregunta}. menciona solo 3 observaciones relevantes")
    return SwarmState(pregunta=state.pregunta, investigacion=respuesta.content)

def analista_agent(state: SwarmState):
    investigacion = state.investigacion
    respuesta = llm.invoke(f"Eres un analista. Resume y analiza esta información:\n{investigacion}")
    return SwarmState(pregunta=state.pregunta, investigacion=state.investigacion, analisis=respuesta.content)

def redactor_agent(state: SwarmState):
    analisis = state.analisis
    respuesta = llm.invoke(f"Eres un redactor profesional. Redacta una respuesta clara basada en este análisis:\n{analisis}")
    return SwarmState(pregunta=state.pregunta, investigacion=state.investigacion, analisis=state.analisis, respuesta_final=respuesta.content)

# Crear el grafo de agentes (enjambre)
graph = StateGraph(SwarmState)


# Inserto y asigno funcion o rol a cada uno de los agentes que van a componer el grafo
graph.add_node("investigador", investigador_agent)
graph.add_node("analista", analiosta_agent)
graph.add_node("redactor", redactor_agent)



#  Definición del flujo (edges)
graph.set_entry_point("investigador")
graph.add_edge("investigador", "analista")
graph.add_edge("analista", "redactor")
graph.add_edge("redactor", END)


# Compilar el grafo
swarm = graph.compile()

# Probar el enjambre de agentes con un diccionario como estado inicial
#estado_inicial = ("pregunta="¿Cuáles son las consecuencias del cambio climático en América Latina?"")

resultado = swarm.invoke({"pregunta":"¿Cuáles son las consecuencias del cambio climático en América Latina?"})

# Mostrar la respuesta final generada por el enjambre
print("Respuesta final generada por el enjambre:\n")
#print(resultado.respuesta_final)
print(resultado)
