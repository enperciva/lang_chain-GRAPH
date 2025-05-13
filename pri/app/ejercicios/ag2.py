
import re
from langchain_community.tools import DuckDuckGoSearchRun, DuckDuckGoSearchResults, WikipediaQueryRun
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper, WikipediaAPIWrapper

from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool

from dotenv import load_dotenv
import os
import warnings
from langchain_google_genai import ChatGoogleGenerativeAI
warnings.filterwarnings("ignore")


load_dotenv()

os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")
llm = ChatGoogleGenerativeAI(model = "gemini-2.0-flash" , temperature=0.1)


# =========================================================================================================
# Tool para hacer busquedas a traves del browser DuckDuckGo
# =========================================================================================================

buscador = DuckDuckGoSearchRun()


# Empaquetar como Tool para que el agente pueda usarla
herramienta = Tool(
    name="DuckDuckGo Search",
    func=buscador,
    description="Usa esta herramienta para buscar información en la web actual."
)


agente = initialize_agent(
    tools=[herramienta],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False
)

p = "biografia completa de {personaje}"


wrapper = DuckDuckGoSearchAPIWrapper (region='cl-es', max_results=3, safesearch='moderate') 
search = DuckDuckGoSearchRun(api_wrapper = wrapper, source='espectaculos') 
salida = search.run('donald trump')

print(salida)

pattern = re.findall(r"title:\s*(.*?)\s*,\s*link:\s*(.*?)\s*,\s*snippet:\s*(.*?)(?=title:|$)", salida, re.DOTALL)

for titulo, link, snippet in pattern:
    print("Título:", titulo.strip())
    print("Link:", link.strip())
    print("Snippet:", snippet.strip())
    print("-" * 40)

#para dar formato a la salida 

""" import re
pattern = r'snippet: (.*?), title: (.*?), link: (.*?)],'
matches = re.findall(pattern, output, re.DOTALL)

for snippet, title, link in matches:
    print(f'Snippet:
    
"""
 

 
# =========================================================================================================
# Tool para hacer busquedas a traves de wikipedia
# =========================================================================================================

""" # Crear un wrapper
 api_wrapper = WikipediaAPIWrapper(lang='es', top_k_results=1, doc_content_chars_max=10000) 
wiki = WikipediaQueryRun(api_wrapper=api_wrapper) 
respuesta = wiki.invoke({'query' : 'juan pablo duarte'})
print(respuesta)
 """
