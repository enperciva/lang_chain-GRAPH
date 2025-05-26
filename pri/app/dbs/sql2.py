# ✅ Requisitos: pip install langchain langgraph sqlalchemy pyodbc
#===================================================================
# Este ejercicio de conectarse a una base de datos mssql
# convierte una pregunta a una sentencia sql
#===================================================================

# Librerias del ambiente de entorno 
import os
import warnings
warnings.filterwarnings("ignore")
from dotenv import load_dotenv, find_dotenv 
import sys
import pandas as pd

# Libreria del modelo llm
from langchain_google_genai import ChatGoogleGenerativeAI

#from langchain.utilities import SQLDatabase
from langchain_community.utilities.sql_database import SQLDatabase
#from langchain_community.utilities import SQLDatabase
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
# from langchain.chat_models import ChatOpenAI
from langgraph.graph import StateGraph, END

# Para gestionar los URL y URI
import urllib

#Libreria sqlalchemy para todo lo concerniente a conexion y manipulacion de objetos de la base de datos
from sqlalchemy import create_engine
import pymssql
import pyodbc

# # 1. Configura conexión a tu base de datos MSSQL (ajusta la URI según tu sistema)
# db = SQLDatabase.from_uri("mssql+pyodbc://usuario:contraseña@DSN_NAME")

load_dotenv()


# Credenciales de api del llm de google 
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")


# Parámetros de conexion a la base de datos
#server = 'LAPTOP-51O5L6KB\\SERVIDORKAW,1433'
server = 'LAPTOP-51O5L6KB\SERVIDORKAW'
database = 'Nivel_Inicial'
driver = 'ODBC Driver 18 for SQL Server'
trusted_connection = 'True'
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

conn = pyodbc.connect(
    driver=driver,
    server=server,
    database=database,
    user = 'sa',
    password = 'kawdaces00p',
    encrypt = encrypt,
    trust_cert = trust_cert,
    TrustServerCertificate='yes'

)


try:


    # --- Configurar row_factory para devolver diccionarios ---
    # Define la función row_factory
    def row_as_dict(cursor, row):
        # Crear un diccionario para cada fila, usando los nombres de las columnas como claves
        columns = [column[0] for column in cursor.description]
        return dict(zip(columns, row))

    # Asignar la función row_factory a la conexión ANTES de crear el cursor
    conn.row_factory = row_as_dict

    # --- Crear el cursor (sin argumentos especiales) ---
    cursor = conn.cursor() # Ya no se usa as_dict=True aquí

    # --- Ejecutar una consulta y obtener resultados como diccionarios ---
    cursor.execute("SELECT TOP 5 ID_Alumno, NombreAlumno FROM NVI_Alumnos;")
    
    for row_dict in cursor: # Las filas ahora serán diccionarios
        print(f"ID: {row_dict['ID_Alumno']}, Nombre: {row_dict['NombreAlumno']}")

    cursor.close()
    conn.close()

except pyodbc.Error as ex:
    sqlstate = ex.args[0]
    print(f"Error al conectar: {sqlstate} - {ex.args[1]}")

cursor.execute("""
    SELECT 
        TABLE_SCHEMA,
        TABLE_NAME,
        COLUMN_NAME,
        DATA_TYPE,
        IS_NULLABLE,
        CHARACTER_MAXIMUM_LENGTH,
        COLUMN_DEFAULT
    FROM INFORMATION_SCHEMA.COLUMNS
    ORDER BY TABLE_SCHEMA, TABLE_NAME, ORDINAL_POSITION
    """)



# Codificar para URL
#odbc_connect = urllib.parse.quote_plus(connection_string)
odbc_connect = pymssql.connect(connection_string)
engine = create_engine(f"mssql+py:///?odbc_connect={odbc_connect}")


# Conectar a la DB
#db = SQLDatabase(engine)
db = SQLDatabase(engine)

sys.exit()

# Obtener info general de tablas y columnas
#schema_info = db.get_table_info()

print("voy por el schema -------------------------------------")
schema_info = db.get_table_info(include_comments=False, get_col_comments=False, ignore_tables=["fn_listextendedproperty"])

print("termine el schema -------------------------------------")

# Define the llm 
llm =  ChatGoogleGenerativeAI (model="gemini-2.0-flash", temperature=0.7) 


print("saliendo ------------------------ \n", engine)


prompt = PromptTemplate.from_template("""
Eres un experto en bases de datos. Convierte la siguiente pregunta en una consulta SQL válida para esta base de datos:

Pregunta: {question}
""")

convert_nl_to_sql = ChatGoogleGenerativeAI(llm=llm, prompt=prompt)

# 3. Define el estado del grafo
class GraphState(dict):
    pass

# 4. Nodo para convertir lenguaje natural a SQL
def convert_to_sql_node(state):
    question = state["question"]
    sql = convert_nl_to_sql.run({"question": question})
    return {"sql_query": sql}

# 5. Nodo para ejecutar la consulta SQL en MSSQL
def execute_sql_node(state):
    sql = state["sql_query"]
    result = db.run(sql)
    return {"result": result}

# 6. Construcción del grafo
workflow = StateGraph(GraphState)

workflow.add_node("convert_to_sql", convert_to_sql_node)
workflow.add_node("execute_sql", execute_sql_node)

workflow.set_entry_point("convert_to_sql")
workflow.add_edge("convert_to_sql", "execute_sql")
workflow.add_edge("execute_sql", END)

app = workflow.compile()

# 7. Ejecutar el grafo con una pregunta en lenguaje natural
pregunta = "¿Cuál es el promedio de edad de los usuarios?"
resultado = app.invoke({"question": pregunta})

print("Resultado:")
print(resultado["result"])
