
import os
from  dotenv import load_dotenv
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate

load_dotenv()

llm = OllamaLLM(model="gemma:2b", temperature=0.1)

template = "Explica brevenebte el siguiente tema de manera sencilla : {tema}"

def explicar_tema(temas):
    prompt = template.format(tema=temas)
    respuesta = llm.invoke(prompt)
    return respuesta 

if __name__ == "__main__":
    resultado = explicar_tema("aves")
    print(resultado)