from langchain_groq import ChatGroq

import getpass
import os

""" if "GROQ_API_KEY" not in os.environ:
    os.environ["GROQ_API_KEY"] = getpass.getpass("Enter your Groq API key: ") """




llm = ChatGroq(
    groq_api_key="",  # 🔑 Tu API aquí
    model_name="deepseek-r1-distill-llama-70b",
    temperature=0.1
)

respuesta = llm.invoke("¿Qué beneficios tiene tener una mascota?")
print(respuesta)
