#===================================================================
# Este ejercicio se utiliza la tecnica de prompts REAC. 
# Esta Tecnica permite la optencion de mejores respuestas de las inferencias
# a partir de como REAC estructura el flujo de acciones de ejecucion de la inferencia a traves de un prompt
#===================================================================

# Librerias para interactuar con el entorno
import config
import os
import warnings
warnings.filterwarnings("ignore")

from dotenv import load_dotenv, find_dotenv 

# Libreria del llm a utilizar 
from langchain_google_genai import ChatGoogleGenerativeAI

# Para operar busquedas en wikipedia
from langchain import Wikipedia

# libreria de mensajes
from langchain_core.messages import HumanMessage, AIMessage


from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType

# Visualizacion y depuracion de documentos
from langchain.agents.react.base import DocstoreExplorer

load_dotenv()

# Credenciales de api del llm de google 
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

# Declara modelo llm
llm = ChatGoogleGenerativeAI(model = "gemini-2.0-flash" , temperature=0.5)

#question = "Quién era el director técnico de la selección nacional de fútbol de Chile cuando ganó la Copa América por primera vez?"

#respuesta = llm.invoke("Quién era el director técnico de la selección nacional de fútbol de Chile cuando ganó la Copa América por primera vez?")
#print(respuesta.content)


# Wikipedia : Es un wrapper de la API de Wikipedia. Retorna el resumen de una página
#            según los keywords de la query. Si no encuentra página, retorna una lista
#            de páginas similares.
#
# DocstoreExplorer: Clase que permite asistir la exploración de un documento.
#                   Tiene los métodos search y lookup.

docstore = DocstoreExplorer(Wikipedia())

# Esta función será utilizada para calcular la edad.
# Notar que recibe un solo argumento.
def substract(numbers)->int:
  'Compute the subtraction between two numbers'
  x = float(numbers.split(',')[0])
  y = float(numbers.split(',')[1])
  return x-y

# Creamos la lista de Tools que le entregaremos al agente.
# Usaremos el método docstore.search para realizar las búsquedas de doucmentos.
# y el método de docstore.lookup para buscar términos en un documento.

tools = [
    Tool(
        name="Search",
        func=docstore.search,
        description="Útil cuando necesitas preguntar con búsqueda"
    ),
    Tool(
        name="Lookup",
        func=docstore.lookup,
        description="Útil cuando necesitas preguntar utilizando una consulta o búsqueda puntual"
    ),
    Tool.from_function(
        name='Substract',
        func=substract,
        description="useful for when you need to compute age by year and the year of birthdate separated by comma. Ex: 2023,1988"
    )
]
""" for tool in tools:
    print(f"{tool=}, tipo={type(tool)}") """

# Inicializamos un ejecutor de agentes.
# Le entregamos el agente, la lista de tools, el modelo LLM, y el agente.
# Para rastrear las acciones, configuramos verbose=True.



react = initialize_agent(agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                         tools=tools,
                         llm=llm,
                         verbose=True)


react.agent.llm_chain.prompt.template = """ Responde las siguientes preguntas lo mejor que puedas. Tienes acceso a las siguientes herramientas:

Search: útil cuando necesitas preguntar algo mediante búsqueda.

Lookup: útil cuando necesitas consultar algo directamente.

Substract: útil cuando necesitas calcular la edad a partir del año actual y el año de nacimiento, separados por coma. Ejemplo: 2023,1988

Usa el siguiente formato:

Pregunta: la pregunta que debes responder

Pensamiento: siempre debes pensar qué hacer

Acción: la acción a realizar, debe ser una de [Search, Lookup, Substract]

Entrada de la acción: la entrada que se le da a la acción

Observación: el resultado de la acción

... (este bloque de Pensamiento/Acción/Entrada de la acción/Observación puede repetirse N veces)

Pensamiento: ahora sé la respuesta final

Respuesta final: la respuesta final a la pregunta original

¡Comienza!

Question: {input}
Thought:{agent_scratchpad} """

repuesta = llm.invoke("a que edad murio juan pablo duarte")

print(repuesta.content)