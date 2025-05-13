import requests
from langchain.prompts import PromptTemplate
import os
from  dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
import warnings
warnings.filterwarnings("ignore")

load_dotenv()

os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

def datospeli(pelicula):
    
    #pelicula = "titanic"

    url = "https://api.themoviedb.org/3/search/movie?query={peli}&include_adult=false&language=en-US&page=1"

    headers = {
        "accept": "application/json",
        "Authorization": ""
    } 
    #respuestas = requests.get(url, headers=headers)
    respuestas = requests.get(url.format(peli=pelicula), headers=headers)

    return respuestas



llm = ChatGoogleGenerativeAI(model = "gemini-2.0-flash" , temperature=0.1)

template = """te voy a enviar datos de varias peliculas. Vas a seleccionar las 3 primeras del grupo de peliculas.
              Vas que darme los datos de fecha de estreno y resumen de la pelicula en español y de manera estructurada
              {rqpelicula}"""

prtemplate = PromptTemplate(input_variables=["rqpelicula"], template=template)

cadena = LLMChain(llm=llm, prompt=prtemplate )

datospeliculas = datospeli("asesino")

#print(datospeliculas.text)

#datossolicitados = cadena.invoke({"rqpelicula" : datospeliculas.text})
datossolicitados = cadena.run(rqpelicula = datospeliculas.text)

print(datossolicitados)














""" peliculas = respuestas.json()

print(len(peliculas['results'][0]['overview'])) """

