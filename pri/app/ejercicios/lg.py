import os
import logging
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_core.messages import HumanMessage
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain_google_genai import ChatGoogleGenerativeAI
# Para operar busquedas en wikipedia
from langchain import Wikipedia
from langchain.agents.react.base import DocstoreExplorer
from langchain.chains import LLMChain

# Libreria para crear los grafos y el estado del mismo.
from langgraph.graph import StateGraph
from typing import TypedDict

# === Cargar entorno ===
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")
logging.basicConfig(level=logging.INFO)

# === LLM ===
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.5)

# === Herramientas ===
docstore = DocstoreExplorer(Wikipedia())

def substract(numbers: str) -> float:
    x = float(numbers.split(',')[0])
    y = float(numbers.split(',')[1])
    return x - y

tools = [
    Tool(name="Search", func=docstore.search, description="Para preguntas generales."),
    Tool(name="Lookup", func=docstore.lookup, description="Para buscar términos específicos."),
    Tool.from_function(name="Substract", func=substract, description="Calcula la diferencia entre dos años.")
]

# === Crear el Prompt Personalizado ===
prompt_template = """Responde las siguientes preguntas lo mejor que puedas. Tienes acceso a las siguientes herramientas:

- **Search**: útil cuando necesitas preguntar algo mediante búsqueda.
- **Lookup**: útil cuando necesitas consultar algo directamente, pero debe realizarse después de haber hecho una búsqueda exitosa.
- **Substract**: útil cuando necesitas calcular la edad a partir del año actual y el año de nacimiento, separados por coma. Ejemplo: 2023,1988.

Usa el siguiente formato:

Pregunta: la pregunta que debes responder.
Pensamiento: siempre debes pensar qué hacer.
Acción: la acción a realizar, debe ser una de [Search, Lookup, Substract].
Entrada de la acción: la entrada que se le da a la acción.
Observación: el resultado de la acción.

¡Comienza!

Pregunta: {input}
Pensamiento: {agent_scratchpad}
"""

# Define el esquema de estado (state_schema)
class AgentState(TypedDict):
    input: str
    output: str

# Crear el grafo con el esquema de estado
workflow = StateGraph(AgentState)


# === Crear un LLMChain con el Prompt Personalizado ===
prompt = PromptTemplate(input_variables=["input", "agent_scratchpad"], template=prompt_template)
llm_chain = LLMChain(llm=llm, prompt=prompt)

# === Crear agente manualmente con herramientas ===
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# === Crear el grafo ===

workflow = StateGraph(state_schema=AgentState)
workflow.add_node("agent", agent)
workflow.set_entry_point("agent")
workflow.set_finish_point("agent")

# === Ejecutar el agente ===
inputs = {"input": "¿A qué edad murió Juan Pablo Duarte?"}
output = workflow.compile().invoke(inputs)

print(f"\n✅ Respuesta final: {output['output']}")
