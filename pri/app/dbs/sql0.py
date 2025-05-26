import os
from dotenv import load_dotenv
import sys

# Libreria del modelo llm
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_experimental.sql import SQLDatabaseChain
from langchain.memory import ConversationBufferMemory
from langchain_community.utilities import SQLDatabase
from langchain.prompts import PromptTemplate
from sqlalchemy import create_engine, text
import pymssql
import pyodbc
import urllib
from app.dbs import conector

# import logging

# logging.basicConfig(level=logging.INFO)
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Añade la carpeta raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


load_dotenv()

# Credenciales de api del llm de google 
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")


# Inicializar modelo y memoria
llm =  ChatGoogleGenerativeAI (model="gemini-2.5-flash-preview-04-17", temperature=0.7) 

#memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Prompt que enseña al modelo cómo interpretar las preguntas
prompt = PromptTemplate.from_template("""
Eres un asistente experto en generar consultas SQL exclusivamente para Microsoft SQL Server.

Dentro de la base de datos, vas a trabajar con los datos de las siguientes tablas:
- CXC_Cliente : Contiene datos de los clientes
- CXC_Factura_M : Datos generales de las facturas
- CXC_Factura_D : Datos con los detalles financieros de las facturas   

Vas a recibir un codigo de factura (Id_Factura) dentro de la pregunta que se te haga y de ese cliente
y vas a determinar el balance actual de esa factura.

la formula para calcular el balance de la factura es :
                                      
   Balance_factura = sum(CXC_Factura_D.precio * CXC_Factura_D.cantidad)      

La respuesta debe de contener el monto calculado                         
                                                                                                                                                  
(Nunca utilices comillas invertidas ni bloques de formato Markdown como ```sql. Solo devuelve SQL limpio.)
                                                             

Pregunta:
{input}
""")

db,engine = conector.conectarse()


""" with engine.connect() as conn:
    result = conn.execute(text("SELECT TOP 5 * FROM CXC_Cliente"))
    rows = result.mappings().all()  # <-- consumir todo aquí
    for row in rows:
        print(row["Nombre"])  # o row.items() """

# Crear el agente
agent = SQLDatabaseChain.from_llm(
    llm=llm,
    db=db,
    prompt=prompt,
    return_intermediate_steps=False,  # si no quieres el SQL
    #memory=memory,
    verbose=False,
)

# Pregunta de ejemplo
respuesta = agent.invoke("¿Cuál es el balance de la Id_Factura 1224 ?")
print(respuesta)
print(respuesta["result"])
 



# ----------------------------------------------------------------------------------------------------
""" 
Tienes acceso a una base de datos MSSQL con las siguientes tablas:

- CC_Facturas_M(ID_Factura, Fecha_Factura, cliente_id)
- facturas_pagadas(cliente_id, fecha_pago, monto_pagado)
- facturas_ajustadas(cliente_id, fecha_ajuste, monto_ajustado)
- clientes(id, nombre)

Reglas del negocio:
- El balance de un cliente es: SUM(facturas) - SUM(pagos) - SUM(ajustes)
- El balance a una fecha considera los valores hasta esa fecha.
- La proyección de facturación puede basarse en la media mensual del último año.

 """
# ----------------------------------------------------------------------------------------------------