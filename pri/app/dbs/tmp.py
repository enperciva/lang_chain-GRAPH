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

import logging

logging.basicConfig(level=logging.INFO)
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Añade la carpeta raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from app.dbs import conector

load_dotenv()

# Credenciales de api del llm de google 
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")


# Inicializar modelo y memoria
llm =  ChatGoogleGenerativeAI (model="gemini-2.0-flash", temperature=0.7) 

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Prompt que enseña al modelo cómo interpretar las preguntas
prompt = PromptTemplate.from_template("""Tienes acceso a una base de datos MSSQL con las siguientes tablas:-CXC_Cliente.En las clausulas select que generes, No uses comillas invertidas. cuando se pregunta por el apellido se refiere en la tabla al campo primer_apellido {chat_history} Pregunta:{input}""")

# Crear el agente
agent = SQLDatabaseChain.from_llm(
    llm=llm,
    db=conector.conectarse(),
    prompt=prompt,
    memory=memory,
    verbose=True,
)

# Pregunta de ejemplo
respuesta = agent.run("¿Cuál es el apellido del cliente de nombre Oscar?")
print(respuesta)





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