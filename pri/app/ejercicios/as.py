from langchain.agents import create_react_agent, AgentExecutor, initialize_agent
#from langchain.agents.agent_toolkits import load_tools
#from langchain.agents import load_tools enb
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain_ollama import OllamaLLM

from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os
from langchain_community.llms import HuggingFaceHub
import warnings

warnings.filterwarnings("ignore")

load_dotenv()
os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv("HUGFACE_TOKEN")

# Instanciamos el modelo

# Crear el modelo
llm = HuggingFaceHub(
    repo_id="google/flan-t5-large",
    task="text-generation",  # ¡esto es clave!
    model_kwargs={"temperature": 0.5, "max_length": 100}
)

# 2. Crear el prompt template
template = "dame el url de 2 sitios web que traten el tema de mascotas"
promptt = PromptTemplate(template=template)

# 3. Cargar las herramientas (SerpAPI)
tools = load_tools(["serpapi"], prompt=promptt, llm=llm)

# 4. Crear el agente
agent = initialize_agent(
    tools=tools, 
    llm=llm,
    #agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,  # Define el tipo de agente
    verbose=True,
    handle_parsing_errors=True
)

# 5. Ejecutar el agente con una pregunta
respuesta = agent.invoke({"input": "vas a buscar 2 sitios web que traten el tema de mascotas"})
print(respuesta)