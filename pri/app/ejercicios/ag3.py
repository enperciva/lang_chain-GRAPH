# herramientas
from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun
from langchain_experimental.tools.python.tool import PythonREPLTool 
# utilitarios
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper, WikipediaAPIWrapper
# agentes
from langchain import hub 
from langchain.agents import Tool, AgentExecutor, initialize_agent, create_react_agent 
# llm y prompts
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate 
# Entono
import os
import warnings
warnings.filterwarnings("ignore")
from dotenv import load_dotenv
load_dotenv()

# Conecta la API de la llm de googleai
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

# Define modelo llm
llm = ChatGoogleGenerativeAI(model = "gemini-2.0-flash" , temperature=0.1)


# Define template
template = """Responde las siguientes preguntas en Italiano lo mejor que puedas.
                Preguntas: {pregunta} 
""" 
prompt_template = PromptTemplate.from_template(template=template)

prompt = hub.pull('hwchase17/react') 
#print(prompt)

"""
Este método te permite extraer y utilizar objetos, como agentes, configuraciones o plantillas, 
que han sido compartidos en LangChain Hub por otros usuarios o creadores o default de langchain. 
En este caso particula 'hwchase17/react' hace referencia a una configuración o componente específico, 
que está relacionado con la funcionalidad.
Esta funcionalidad es particularmente útil cuando deseas implementar lógicas complejas o específicas 
sin tener que desarrollar todo desde cero. Al aprovechar los componentes compartidos en LangChain Hub,
puedes enriquecer tus aplicaciones con funcionalidades avanzadas, facilitando el desarrollo de soluciones
 basadas en modelos de lenguaje grande (LLM) y otras herramientas de procesamiento de lenguaje natural (NLP).
 
 """
#=========================================================================
 #1. Primera herramienta Python REPL Tool 
 #=========================================================================

python_repl = PythonREPLTool() 
python_repl_tool = Tool( 
    name='Python REPL', 
    func=python_repl.run, 
    description="Útil cuando necesitas usar Python para responder una pregunta. Debes ingresar código Python." 
)
#=========================================================================
#2. Segunda herramienta Wikipedia Tool 
#=========================================================================
api_wrapper = WikipediaAPIWrapper() 

wikipedia = WikipediaQueryRun(api_wrapper=api_wrapper) 

wikipedia_tool = Tool( 
    name="Wikipedia", 
    func = wikipedia.run, 
    description= 'Útil cuando necesitas buscar un tema, país o persona en Wikipedia.'
)
#=========================================================================
#3. Tercera herramienta DuckDuckGo Search Tool 
#=========================================================================
search = DuckDuckGoSearchRun() 
duckduckgo_tool = Tool( 
    name='DuckDuckGo Search', 
    func=search.run, 
    description="Útil cuando necesitas realizar una búsqueda en internet para encontrar información que otra herr"
)

# Determina la caja de herramientas
cajaherramientas = [python_repl_tool, wikipedia_tool, duckduckgo_tool] 

# Declara el agente que va a utilizar de la caja de herramientas
agent = create_react_agent(llm, cajaherramientas, prompt) 

# Ejecuta el agente 
agent_executor = AgentExecutor( 
    agent = agent, 
    tools = cajaherramientas, 
    verbose = True, 
    handle_parsing_errors=True, 
    max_iterations=10 
)

question = 'determina los numeros primeros en el rarngo del  al 100'
output = agent_executor.invoke({ 
                                'input': prompt_template.format(pregunta=question) 
                               }) 

print(output)