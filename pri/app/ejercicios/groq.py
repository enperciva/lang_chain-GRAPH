from langchain.llms import BaseLLM
import requests

class GroqLLM(BaseLLM):
    def __init__(self, api_key: str, endpoint: str):
        super().__init__()
        self.api_key = api_key
        self.endpoint = endpoint

    @property
    def _llm_type(self):
        return "text"  # Puede ser "chat" o "text", dependiendo de la API de Groq

    def _generate(self, prompts: list, stop: list = None) -> str:
        """
        Genera texto usando la API de Groq.
        """
        prompt = prompts[0]  # Asume que recibes una lista de prompts

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "inputs": prompt,
            "temperature": 0.7,  # O puedes ajustar esto
            "max_tokens": 200,  # Cambia según lo que necesites
            # Otros parámetros de la API de Groq si son necesarios
        }

        response = requests.post(self.endpoint, json=payload, headers=headers)

        if response.status_code == 200:
            return response.json().get('text', '')  # Asegúrate de que el campo 'text' sea correcto
        else:
            raise Exception(f"Error: {response.status_code}, {response.text}")

# Crear la instancia del modelo GroqLLM con tus credenciales
groq_llm = GroqLLM(api_key="", endpoint="https://api.groq.com/openai/v1/chat/completions")

# Crear una cadena en LangChain con un prompt simple
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

prompt_template = PromptTemplate(input_variables=["input"], template="Genera un resumen de: {input}")
llm_chain = LLMChain(llm=groq_llm, prompt=prompt_template)

# Ejecutar la cadena y obtener la respuesta
response = llm_chain.run("Un artículo sobre los avances de IA en 2025")
print(response)
