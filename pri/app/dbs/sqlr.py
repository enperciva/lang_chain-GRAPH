# Requisitos:
# pip install langchain openai chromadb sqlalchemy pymssql
import os
from dotenv import load_dotenv
import sys
from sqlalchemy import create_engine, inspect, text
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
#from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
import os

# Librerias del enbbeding y del vectorstore
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings

load_dotenv()

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Credenciales de api del llm de google 
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

# ------------------ 1. CONECTAR A MSSQL Y EXTRAER METADATOS ------------------
from app.dbs import conector
import importlib.util
_, engine = conector.conectarse()

inspector = inspect(engine)

def get_schema_info():
    schema_texts = []
    for table in inspector.get_table_names():
        cols = inspector.get_columns(table)
        col_descriptions = ', '.join([f"{col['name']} ({col['type']})" for col in cols])
        schema_texts.append(f"Tabla: {table}\nColumnas: {col_descriptions}")
    return schema_texts

schema_documents = get_schema_info()

print(schema_documents)

sys.exit()

# ------------------ 2. CREAR VECTORSTORE CON CHROMA ------------------


#embeddings = OpenAIEmbeddings()
embeddings = FastEmbedEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

docs = [Document(page_content=text) for text in schema_documents]
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
split_docs = splitter.split_documents(docs)

vectorstore = Chroma.from_documents(split_docs, embeddings, persist_directory="chroma_db")
retriever = vectorstore.as_retriever()

# ------------------ 3. USAR LLM PARA RESPONDER PREGUNTAS ------------------
llm = ChatOpenAI(model="gpt-4", temperature=0)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True
)

# ------------------ 4. PREGUNTA DEL USUARIO ------------------
pregunta = input("Escribe tu pregunta sobre la base de datos MSSQL: ")

respuesta = qa_chain(pregunta)
print("\n🧠 Respuesta del modelo:")
print(respuesta["result"])

# ------------------ 5. OPCIONAL: GENERAR Y EJECUTAR SQL ------------------
# Nueva pregunta con intención de obtener SQL
system_prompt = """
Eres un experto en bases de datos MSSQL. A partir de una pregunta en lenguaje natural, 
genera solamente la consulta SQL necesaria para obtener la información de la base. 
NO EXPLIQUES NADA. SOLO DEVUELVE LA CONSULTA SQL.
"""

sql_llm = ChatOpenAI(model="gpt-4", temperature=0)
from langchain.prompts import ChatPromptTemplate

template = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", pregunta)
])

sql_query = sql_llm(template.format_messages())[0].content.strip()

print("\n📝 Consulta SQL generada:")
print(sql_query)

# Confirmación para ejecutar
confirmar = input("\n¿Deseas ejecutar esta consulta en la base de datos MSSQL? (s/n): ")
if confirmar.lower() == "s":
    try:
        with engine.connect() as conn:
            result = conn.execute(text(sql_query))
            rows = result.fetchall()
            print("\n📊 Resultados:")
            for row in rows:
                print(dict(row._mapping))
    except Exception as e:
        print(f"❌ Error ejecutando la consulta: {e}")
