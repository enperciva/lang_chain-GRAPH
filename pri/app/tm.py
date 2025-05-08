# Librerias del ambiente de entorno 
import os
import warnings
warnings.filterwarnings("ignore")
from dotenv import load_dotenv, find_dotenv 

import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

try:
    # Verificar si la API está correctamente configurada
    #genai.configure(os.getenv("GEMINI_API_KEY"))
    model =genai.GenerativeModel("gemini-2.0-flash")
    response = model.invoke("¿Qué es la inteligencia artificial?")
    print(response.text)
except Exception as e:
    print("Error:", e)