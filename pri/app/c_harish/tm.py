from sqlalchemy import create_engine, inspect
import os


import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


base_dir = os.path.dirname(os.path.abspath(__file__)) + os.sep
db_path = os.path.join(base_dir, '../../dbs/', 'example.db') 
engine = create_engine(f"sqlite:///{db_path}")

print("base ---------------", base_dir)
print("path -----------------", db_path)
print("engine----------------------",engine)

Session = sessionmaker(bind=engine)
session = Session()
# Crear base declarativa
#Base = declarative_base()

inspector = inspect(engine)

# Obtener nombres de todas las tablas
tablas = inspector.get_table_names()
print(tablas)

# Obtener columnas de una tabla específica
columnas = inspector.get_columns("orders")
for columna in columnas:
    print(columna["name"], columna["type"])
