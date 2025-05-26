import os
from dotenv import load_dotenv
from langchain_experimental.sql import SQLDatabaseChain
#from langchain.sql_database import SQLDatabase
from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine, text, Column, Integer, String, ForeignKey, Float, Table, MetaData
from sqlalchemy.orm import sessionmaker, relationship, declarative_base, Session
import pymssql
import pyodbc
import urllib

# Parámetros de conexion a la base de datos
#server = 'LAPTOP-51O5L6KB\\SERVIDORKAW,1433'
server = 'LAPTOP-51O5L6KB\SERVIDORKAW'
database = 'Imp_CXC'
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
#    f"Trusted_Connection={trusted_connection};"
    f"UID={username};"
    f"PWD={password};"
    f"Encrypt={encrypt};"
    f"TrustServerCertificate={trust_cert};"
)

def conectarse():
    # Codifica la cadena de conexión completa para URL
    odbc_connect = urllib.parse.quote_plus(connection_string)

    # --- Crear el Motor de SQLAlchemy ---
    try:
        engine = create_engine(f"mssql+pyodbc:///?odbc_connect={odbc_connect}", connect_args={'convert_unicode': True},echo=False)
    
        # --- Probar la conexión ---
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("¡Conexión exitosa a la base de datos SQL Server!")
            for row in result:
                print(f"Resultado de la consulta de prueba: {row}")

    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")

    Base = declarative_base()

# Definition sqlalchemy of the Users table
    class User(Base):
        __tablename__ = "cxc_cliente"
        cliente_id = Column(Integer, primary_key=True, index=True)
        nombre = Column(String(40), nullable=False)
        primer_apellido = Column(String(30), nullable=False)
        segundo_apellido = Column(String(60), nullable=False)
        direccion = Column(String(20), nullable=False)
    
    
    # guarda los datos de la reflexion en el contexto de sqlarchmey
    metadata = MetaData()
    metadata.reflect(bind=engine)
    """
        misession01 = sessionmaker(bind=engine)
        with misession01() as session:
            esulta = session.execute(text("SELECT top 5 * FROM CXC_Cliente")) 
       
    msesion = Session(engine)
    rr = msesion.query(User).limit(8).all()

    for i in rr:
        print(i.nombre)
     """

    db = SQLDatabase(engine)

    return db, engine

""" 
# para cargar y hacer refelexion de tablas de la base de datos a sqlarchemy como ORM 
from sqlalchemy.ext.automap import automap_base
Base = automap_base()

# Carga la estructura de la BD real
Base.prepare(engine, reflect=True)

# Ahora puedes acceder a la clase generada automáticamente:
Cliente = Base.classes.CXC_Cliente """

# Hace refrexion a toda la base de datos y no tienes que usar tablas ORM locales
# metadata.reflect(bind=engine)

# Crea una fábrica de sesiones para interactuar con la base de datos mediante ORM (consulta, inserción, actualización, etc.).
# Session = sessionmaker(bind=engine)

#-------------------------------------------------------------------------------------------------
# metodo core para usar sqlarchemy sin clases ORM
#-------------------------------------------------------------------------------------------------
# Reflejar base
# metadata = MetaData()
# metadata.reflect(bind=engine)

# # Acceder a la tabla reflejada
# clientes = metadata.tables["cxc_cliente"]

# # Crear una consulta
# stmt = select(clientes).where(clientes.c.saldo > 50000)


#-------------------------------------------------------------------------------------------------
# metodo core para usar sqlarchemy con clases ORM
#-------------------------------------------------------------------------------------------------

# Session = sessionmaker(bind=engine)