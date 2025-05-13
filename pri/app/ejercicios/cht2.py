#===================================================================
# Este ejercicio de como se interactua con un chatbox, sobre
# un tema en particular que se le defina.
#===================================================================

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_ollama import OllamaLLM
from langchain_community.llms import HuggingFaceHub
import warnings
import sys
import os
from dotenv import load_dotenv

load_dotenv()

warnings.filterwarnings("ignore")


os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv("HUGFACE_TOKEN")

# Instanciamos el modelo

# Crear el modelo
llm = HuggingFaceHub(
    repo_id="google/flan-t5-large",
    task="text-generation",  # ¡esto es clave!
    model_kwargs={"temperature": 0.5, "max_length": 100}
)

icapital = input("pais : ")

template = "¿Cuál es la capital de {pais}?"

prompt = template.format(pais=icapital)

respuesta = llm.invoke(prompt)

print(respuesta)

sys.exit()


prompt = ChatPromptTemplate.from_messages([ MessagesPlaceholder(variable_name = "chat_history"),

            ("human", "{input}")  
            
            ])


#Crear Cadena de conversacion

chain = prompt | llm

def ejecutar_chatbox():
    print("Bienvenido a este chatbox. Para abandonarlo escribe 'salir")
    chat_history = []

    while True:
        #definimos el input del usuario
        user_input = input('tu :')
        if user_input == 'salir':
            print("hasta luego. gracias por conversar")
            break

        respuesta = chain.invoke({
            "input" : user_input,
             "chat_history": chat_history        })


        chat_history.append(HumanMessage(content=user_input))     
        chat_history.append(AIMessage(content=respuesta))


        print(f"chatbox : {respuesta} ")


if __name__ == "__main__":
    ejecutar_chatbox()