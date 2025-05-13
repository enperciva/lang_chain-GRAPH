#===================================================================
#Ejercicio para conectarse y trabajar con bases de datos MSSQL
#===================================================================

# Librerias para interactuar con el entorno
import os
import warnings
warnings.filterwarnings("ignore")
from dotenv import load_dotenv, find_dotenv 

# Para gestionar los URL y URI
import urllib

# Librerias para conectarse y agenciar base de datos 
from langchain_community.utilities.sql_database import SQLDatabase
from sqlalchemy import create_engine
from langchain.agents.agent_toolkits import create_sql_agent
from langchain_experimental.sql import SQLDatabaseChain
from langchain.agents.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
import pyodbc

# libreria de prompts 
from langchain.prompts import PromptTemplate

load_dotenv()

# Libreria del llm a utilizar 
from langchain_google_genai import ChatGoogleGenerativeAI

# Credenciales de api del llm de google 
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

# Declara modelo llm
llm = ChatGoogleGenerativeAI(model = "google/flan-t5" , temperature=0.5)

# Parámetros de conexion a la base de datos
server = 'LAPTOP-51O5L6KB\\SERVIDORKAW'
database = 'Nivel_Inicial'
driver = 'ODBC Driver 18 for SQL Server'
trusted_connection = 'yes'
encrypt = 'yes'
trust_cert = 'yes'
username = 'sa'
password = 'kawdaces00p'

# Cadena de conexión codificada
connection_string = (
    f"DRIVER={{{driver}}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"Trusted_Connection={trusted_connection};"
    f"Encrypt={encrypt};"
    f"TrustServerCertificate={trust_cert};"
)

llm = ChatGoogleGenerativeAI(model = "gemini-2.0-flash" , temperature=0.5)

# Codificar para URL
odbc_connect = urllib.parse.quote_plus(connection_string)
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={odbc_connect}")

# Seleccionar SQLDatabase object 
db = SQLDatabase(engine,schema = 'Nivel_inicial')

template ="""  "Contesta las preguntas que se te hagan. Utiliza la tabla NVI_Alumnos.






            {question}" 
            
            
            
            
            
            
            
            """

prompt = PromptTemplate.from_template(template=template)

agent_executor = create_sql_agent(
    llm=llm,
    toolkit=SQLDatabaseToolkit(db=db, llm=llm),
    verbose=False,
)

apellido = "cuantos alumnos de la tabla dbo.NVI_Alumnos son varones y cuantos son hembras. utiliza el campo sexo para determinarlo"
resultado = agent_executor.invoke({"input" : apellido})

print(resultado)
""" 
Pautas:
Genera una consulta SQL sintácticamente correcta en el dialecto {dialect} que responda a la pregunta del usuario.
Proporciona solo la consulta SQL como salida.
No incluyas formato markdown (por ejemplo, no uses sql ni )
No agregues prefijos como "SQLQuery:" ni ningún otro texto adicional.
Limita la consulta a los primeros {top_k} resultados, a menos que el usuario especifique lo contrario.
Ordena los resultados por una columna relevante, si aplica, para devolver los ejemplos más interesantes.
Nunca selecciones todas las columnas (SELECT *); incluye solo aquellas relevantes a la pregunta.
Usa únicamente los nombres de columna proporcionados en el esquema. Evita consultar columnas que no existen.
Si la pregunta del usuario no puede ser respondida con el esquema o los datos proporcionados, responde con:
"No tenemos datos relacionados en la base de datos". """