#from langchain.llms import OpenAI
from dotenv import load_dotenv

from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain_ollama import OllamaLLM
from langchain_community.llms import HuggingFaceHub
import warnings
warnings.filterwarnings("ignore")

import os

load_dotenv()

#OPENAI_API_KEY = ""

#print(os.environ["OPENAI_API_KEY"])
#print(os.environ["OSCARAI"])

#template = "eres un traductor de texto que traduces del {idiomainicial} al {idiomafinal} el texto {texto}"
template = "eres un traductor de texto que traduces del {idiomainicial} al {idiomafinal} el texto {texto}. La respuesta solo debe presentar el texto de la traduccion"

texto="Hola, como te sientes"
idiomai = "castellano"
idiomaf = "frances"

prompt_template = PromptTemplate( template=template, varentrada=[idiomai,idiomaf,texto])

#llm = ChatOpenAI(temperature=0.1, model_name="gpt-3.5-turbo")

llm = OllamaLLM(model="gemma:2b",temperature=0.1)



chain = LLMChain(llm=llm, prompt=prompt_template )

respuesta = chain.invoke(input={"idiomainicial":idiomai, "idiomafinal":idiomaf, "texto":texto})

print(respuesta)