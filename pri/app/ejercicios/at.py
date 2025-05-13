#importamos librerias
import os
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.tools import BaseTool, StructuredTool, tool
from langchain_core. prompts import ChatPromptTemplate, MessagesPlaceholder
from  dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import OllamaLLM
from langchain.chains import LLMChain
import warnings
import os
import re

os.environ["LANGCHAIN_NO_COLOR"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "true"


warnings.filterwarnings("ignore")
load_dotenv()

os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

def limpiar_ansi(texto):
    return re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', texto)    

## Creacion de herramientas

@tool
def add(a:int, b:int) -> int:
  """Adicionar dos numeros."""
  return a+b

  add.args_schema.model_json_schema()

@tool
def multiply(a:int, b:int) -> int:
  """Multiplicar dos numeros."""
  return a*b

@tool
def square(a:int) -> int:
  """Calcular el numero al cuadrado."""
  return a*a

@tool
def cube(a:int) -> int:
  """elevar al cubo."""
  a= int(a)
  return a*a*a


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", """ Eres un asistente matemático especializado. Utiliza únicamente las herramientas disponibles para responder preguntas relacionadas con matemáticas de manera precisa y concisa.

          Si no cuentas con una herramienta específica para resolver una pregunta, infórmalo claramente, indica que no puedes responder y evita realizar cualquier invocación innecesaria.

          Proporciona solo la respuesta en el formato más directo posible. Por ejemplo:
          Human: ¿Cuánto es 1 + 1?
          AI: 2
        """),

        ("human", "{input}"),

      MessagesPlaceholder("chat_history", optional=True),


      MessagesPlaceholder("agent_scratchpad")

     ]
)

#elige el modelo LLM

llm = ChatGoogleGenerativeAI(model = "gemini-2.0-flash" , temperature=0.1)

#configure el kit de herramientas

tolkit = [add, multiply,square, cube]

#construimos el agebte LLM
agent = create_openai_tools_agent(llm , tolkit, prompt)

#crear ejecutor
agent_executor = AgentExecutor(agent=agent, tools=tolkit, verbose=False)
     

""" result = agent_executor.invoke({"input": "Cual es el area de la tierra"})
print(limpiar_ansi(result['output'])) """
     

result = agent_executor.invoke({"input": "indicame cuanto es (41 + 3 ) * 2"})
print(result)
     

