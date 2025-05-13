from langchain_core.messages import HumanMessage, AIMessage,SystemMessage

from  dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import os
import warnings
warnings.filterwarnings("ignore")
load_dotenv()

os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

llm = ChatGoogleGenerativeAI(model = "gemini-2.0-flash" , temperature=0.1)



# El mensaje que enviar el humano
htemplate = "como se prepara el pie de manzana"

#Define tipos de mensajes que van al chatbox
mensajes = [
            SystemMessage(content="eres un chef y respondes todo en contexto culinario. las respuestas deben tener una extructura textual para facilitar su lectura "),
            HumanMessage(content=htemplate)
           ]

respuesta = llm.invoke(mensajes)


#print(respuesta.content)