#===================================================================================
# El siguiente ejercicio se trata de un chatbox con memoria
#===================================================================================

# Librerias para interactuar con el entorno
import os
import warnings
warnings.filterwarnings("ignore")
from dotenv import load_dotenv, find_dotenv 
load_dotenv()

# Librerias requeridas para el chatbox (modelo llm, prompt, memoria)
from langchain.prompts import PromptTemplate 
from langchain.chains import LLMChain 
from langchain.memory import ConversationBufferMemory 

# Libreria del llm a utilizar 
from langchain_google_genai import ChatGoogleGenerativeAI

# Credenciales de api del llm de google 
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

# Declara modelo llm
llm = ChatGoogleGenerativeAI(model = "gemini-2.0-flash" , temperature=0.5)

""" 
# Configurar memoria 
memory = ConversationBufferMemory (memory_key="historial_del_chat", return_messages=True)

# Crear plantilla para el chat 
template = La siguiente es una conversación amigable entre un humano y un asistente. 
    Historial de la conversación: {historial_del_chat} 
    Humano: {input} 
   

# Creando los agentes del dialogo del chatbox
prompt = PromptTemplate( 
                        input_variables=["chat_history", "input"], 
                        template=template 
                        )

# Crear la cadena con memoria y plantilla 
conversation = LLMChain( 
                        llm=llm, 
                        prompt=prompt, 
                        memory=memory, 
                        verbose=True 
                        ) 


# script de la conversación 
print(conversation.predict(input="¿Qué país ha ganado más mundiales de fútbol?")) 
print(conversation.predict(input="Nombrame 10 jugadores históricos de esa selección"))
print(conversation.predict(input="¿De qué color es su camiseta?"))






 """

#===================================================================================
# El siguiente ejercicio el chatbox se va a expresar sentimientos y analiis de texto
#===================================================================================


# Crear plantilla para análisis de sentimientos 
sentiment_template = """Analiza el sentimiento del siguiente texto y clasifícalo positivo, negativo o neutral. 
                        Proporciona también una explicación de tu análisis. 

                        Texto: {texto} 
                        Formato de respuesta: 
                        Sentimiento: [clasificación] 
                        Explicación: [tu análisis]""" 

sentiment_prompt = PromptTemplate(      
                        input_variables=["texto"],                  
                        template=sentiment_template 
                        )

# Crear la cadena con memoria y plantilla 
analisis_chain = LLMChain( 
                        llm=llm, 
                        prompt=sentiment_prompt,              
                        verbose=False 
                        ) 
# Crea cadena para detectar sentimiento del texto y clasificar


# Envia texto y espera valoracion y analisis del mismo

texto_a_evaluar = "El restaurante tiene cosas que mejorar. La musica estaba muy alta y los camareros se desciuidan "

respuesta = analisis_chain.predict(texto=texto_a_evaluar)

print(respuesta)