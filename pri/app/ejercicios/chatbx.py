from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_ollama import OllamaLLM
from langchain_community.llms import HuggingFaceHub
from dotenv import load_dotenv
import os
import warnings

warnings.filterwarnings("ignore")

load_dotenv()

os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv("HUGFACE_TOKEN")

# Crear el modelo
llm = HuggingFaceHub(
    repo_id="google/gemma-3-1b-it",
    task="text-generation",  # ¡esto es clave!
    model_kwargs={"temperature": 0.5, "max_length": 100}
)

prompt = ChatPromptTemplate.from_messages([ 

            ("system", "Eres un chatbox que e gusta hacer preguntas"),
            ("human", "{input}"),

            MessagesPlaceholder(variable_name = "chat_history")

            ])

#Crear Cadena de conversacion

chain = prompt | llm

def ():
    print("Bienvenido a este chatbox. Para abandonarlo escribe 'salir")
    chat_history = []

    while True:
        #definimos el input del usuario
        user_input = input('tu :')
        if user_input == 'salir':
            print("hasta luego. gracias por conversar")
            break

        respuesta = chain.invoke(
            {"input" : user_input,
            "chat_history": chat_history        
            })


        chat_history.append(HumanMessage(content=user_input))     
        chat_history.append(AIMessage(content=respuesta))


        print(f"chatbox : {respuesta} ")


if __name__ == "__main__":
    ejecutar_chatbox()