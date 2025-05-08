# Librerias del ambiente de entorno 
import os
import warnings
warnings.filterwarnings("ignore")
from dotenv import load_dotenv, find_dotenv 
import requests
import google.generativeai as genai
from  dataclasses import dataclass

from langgraph.graph import StateGraph, END

# Libreria del modelo llm
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

# Configura tu API key de Google Gemini
# Credenciales de api del llm de google 
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# API Key de OpenWeatherMap
OPENWEATHERMAP_API_KEY = os.getenv("OPEN_WEAGHER_API")

# Estado inicial
@dataclass
class WeatherState:
    user_message: str = ""
    city: str = ""
    weather_info: str = ""
    final_response: str = ""

# Función: Llama a Gemini para extraer la ciudad del mensaje
def extract_city(state: WeatherState):      
    user_msg = state.user_message 
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(f"Extrae solo el nombre de la ciudad de esta frase: '{user_msg}'")
    state.city = response.text.strip()
   
    return state

# Función: Consulta la API del clima
def get_weather(state: WeatherState):    
    city = state.city
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHERMAP_API_KEY}&units=metric&lang=es"
    response = requests.get(url)
    if response.status_code != 200:
        state["weather_info"] = f"No se pudo obtener el clima para {city}."
    else:
        # recopila los valores necesarios del json
        data = response.json()
        desc = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        state.weather_info = f"En {city} hay {desc} con {temp}°C (sensación de {feels_like}°C)."
    return state

# Función: Gemini redacta una respuesta final amigable
def reply_with_weather(state: WeatherState):
    weather_info = state.weather_info
    #weather_info = state.get("weather_info", "")
    print("da informacion")
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(f"Redacta una respuesta amable para un usuario que pregunta por el clima. Info: {weather_info}")
    state.final_response = response.text.strip()

    return state


# Construir el grafo de LangGraph
builder = StateGraph(WeatherState)

#===================================================================================
# Lo siguiente son los nodos del grafo
#===================================================================================

builder.add_node("ExtractCity", extract_city)
builder.add_node("GetWeather", get_weather)
builder.add_node("Reply", reply_with_weather)


#===================================================================================
# El siguiente es el flujo del grafo
#===================================================================================
builder.set_entry_point("ExtractCity")

builder.add_edge("ExtractCity", "GetWeather")

builder.add_edge("GetWeather", "Reply")

builder.add_edge("Reply", END)

#===================================================================================
# Fin del flujo del grafo
#===================================================================================

graph = builder.compile()

elclimade = WeatherState({"user_message" :"Habla del clima en Paris"})

estado_final = graph.invoke(elclimade)

print(estado_final)