#===================================================================================
# El siguiente ejercicio se trata sobre el uso de agentes y herramientas personalizadas
#===================================================================================

# Librerias para interactuar con el entorno
import os
import warnings
warnings.filterwarnings("ignore")
from dotenv import load_dotenv, find_dotenv 

# Declaracion de librerias de las clases para manejo de los agentes
from langchain.agents import Tool, initialize_agent, AgentType 
from datetime import datetime 
 
 # Libreria del llm a utilizar 
from langchain_google_genai import ChatGoogleGenerativeAI

# Libreria de regular expressions 
import re

load_dotenv()

# Credenciales de api del llm de google 
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

# Declara modelo llm
llm = ChatGoogleGenerativeAI(model = "gemini-2.0-flash" , temperature=0.5)





def remove_ansi(text):
    ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)

# Función para obtener la hora actual 
def get_current_time(_input=None):     #Acepta un argumento pero no lo usa 
    return datetime.now().strftime("%H:%M:%S")


#Función para calcular la suma de números 
def calculate_sum(numbers_str): 
    try: 
        numbers = [float(n) for n in numbers_str.split()] 
        return str(sum(numbers)) 
    except Exception as e:
        return "Error: Por favor proporciona números separados por espacios"


# Definir herramientas personalizadas 
tools = [ 
            Tool( 
                name="Hora Actual", 
                func=get_current_time, 
                description="Útil para obtener la hora actual" 
            ), 
            Tool( 
                name="Calculadora de Suma", 
                func=calculate_sum, 
                description="Suma una lista de números separados por espacios" 
            )
        ]

# Inicializar el agente 
agent = initialize_agent( 
                            tools=tools, 
                            llm=llm, 
                            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, 
                            verbose=False 
                        )

# Ejemplo de uso del agente 
respuesta = agent.run("¿Qué hora es ahora?")

print((respuesta))


respuesta = agent.run("Suma los siguientes números: 10 20 30 40")

print((respuesta))