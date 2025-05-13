import os
from  dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.chains import LLMChain
load_dotenv()

os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")


# Crear las plantillas de mensajes
system_message = SystemMessagePromptTemplate.from_template(
    """eres un asistente que dice el sexo del personaje que se te especifique.

    
    """
)
human_message = HumanMessagePromptTemplate.from_template("{product_name}")

# Crear el prompt de chat
chat_prompt = ChatPromptTemplate.from_messages([system_message, human_message])

# Instanciar el modelo de chat
#llm = ChatOpenAI(temperature=0.5)salir
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.1)

# Crear la cadena
#chain = LLMChain(llm=llm, prompt=chat_prompt)
chain = chat_prompt | llm

print("para terminar digite 'salir' ")

while True:

    tema = input("diga : ")
    # Ejecutar la cadena
    input_data = {'product_name': tema}

    if tema == 'salir':
        print("me quiete")
        break
    else:
    
        respuesta = chain.invoke(tema)
        print(respuesta)
