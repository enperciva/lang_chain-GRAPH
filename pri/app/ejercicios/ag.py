#from langchain_groq import ChatGroq

from dotenv import load_dotenv
import os
#from langchain_experimental.utilities import PythonREPL
from langchain_experimental.tools.python.tool import PythonREPLTool

#from langchain.tools.python.tool import PythonREPLTool
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_experimental.agents.agent_toolkits import create_python_agent


from langchain.tools import BaseTool, StructuredTool, tool
from langchain.chains import LLMChain

from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

llm = ChatGoogleGenerativeAI(model = "gemini-2.0-flash" , temperature=0.1)

ptool = PythonREPLTool()

agente = create_python_agent( llm = llm, 
                                    tool = ptool,
                                    verbose = True )

prompt = "crea un diccionario con los valores : azul es 1, verde es 2, blanco es 3"



resultado = agente.invoke(prompt)



#resultado = presultado.run("print([i for i in range(1, 50) if i % 10 == 0])")

print(resultado["output"])

