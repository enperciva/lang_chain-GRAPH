#===================================================================================
# El siguiente ejercicio se trata de la implementacion de la clase PYNDANTIC para obtener 
# respuestas estructuradas de las solicitudes a los llms.
#===================================================================================
# Librerias del ambiente de entorno 
import os
import warnings
warnings.filterwarnings("ignore")
from dotenv import load_dotenv, find_dotenv 

load_dotenv()

# Libreria de clases del modulo pydantic
from pydantic import BaseModel, Field 

# Declaracion del llm
# Libreria del modelo llm
from langchain_google_genai import ChatGoogleGenerativeAI


# Credenciales de api del llm de google 
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

llm =  ChatGoogleGenerativeAI (model="gemini-2.0-flash", temperature=0) 

class Country (BaseModel): 
    """Information about a country""" 
    name: str = Field(description="name of the country") 
    language: str = Field(description="language of the country") 
    capital: str = Field(description="Capital of the country") 

structured_llm = llm.with_structured_output(Country) 

structured_llm = structured_llm.invoke("Hablame de Francia")

print(structured_llm)