#===================================================================================
# El siguiente ejercicio vamos a hacer consultas de varios documentos de fuentes diferentes
#===================================================================================

# Librerias para interactuar con el entorno
import os
import warnings
warnings.filterwarnings("ignore")
#cargar variables de entorno desde un archivo 
from dotenv import load_dotenv, find_dotenv 

# Esta libreria es la que hacer un merge de los diferentes tipos de documentos
from langchain_community.document_loaders.merge import MergedDataLoader 

# Esta libreria carga los documentos por tipo
from langchain_community.document_loaders import WebBaseLoader, PyPDFLoader, CSVLoader, TextLoader 

# Librerias del enbbeding y del vectorstore
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_community.vectorstores import Chroma

# Clase RunnablePassthrough
from langchain_core.runnables import RunnablePassthrough,RunnableMap

# Toma la respuesta de un invoke y extrae solo el texto
from langchain_core.output_parsers import StrOutputParser

# llm
from langchain_google_genai import ChatGoogleGenerativeAI

# Cuando se van a cargar sitios web, es recomendable definir USER_AGENT porque algunas webs lo exigen.
os.environ["USER_AGENT"] = "Mozilla/5.0 (compatible; MyBot/1.0; +https://mydomain.com/bot)"


load_dotenv()
# Credenciales de api del llm de google 
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")



loader_web = WebBaseLoader("http://localhost/kbaw/") 
loader_pdf = PyPDFLoader("C:\\Box\\flowise\\datos\\archivos\\bsebo.pdf") 
loader_csv = CSVLoader("C:\\Box\\flowise\\datos\\archivos\\dada.csv") 
loader_txt = TextLoader("C:\\Box\\flowise\datos\\archivos\\kant.txt") 
loader_all = MergedDataLoader(loaders=[loader_web, loader_pdf, loader_txt, loader_csv])
all_docs = loader_all.load() 

# Determinar cuantos documentos contiene la variable contenedora all_docs

print(len(all_docs))

# Para imprimir el contenido de todos los documentos
for doc in all_docs:
    print(doc)
    print()

# Libreria del segmentador de documentos
from langchain.text_splitter import RecursiveCharacterTextSplitter 

# Libreria del embedding de Ollama
from langchain_community.embeddings import OllamaEmbeddings

# Define las propiedades de segmentacion de los documentos
text_splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 80) 

chunks = text_splitter.split_documents(all_docs) 

#embed_model = FastEmbedEmbeddings(model_name="text-embedding-005")
embed_model = FastEmbedEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
#embed_model = OllamaEmbeddings(model="nomic-embed-text")   

vectorstore = Chroma.from_documents(embedding = embed_model,
                                       documents=all_docs,
                                       persist_directory="C:\\Box\\flowise\\datos\\vdocs",
                                       collection_name="docus")

# imprimir cantidad de vectores que se han creado
len(vectorstore) 

# Declarar el retriever que buscara los datos 



from langchain_core.prompts import ChatPromptTemplate 


#Prompt 
template = """Responde las preguntas en el siguiente contexto {context}.
            Las respuestas deben contener el documento de donde extraiste la respuesta.
            Si no puedes responder basándote en el contexto, siempre debes responder:
            No puedo responder la pregunta con el contexto proporcionado.           
            Question: {question} """  

# Integrar el template al prompt
prompt = ChatPromptTemplate.from_template(template) 

# Chain del retriever con el llm y el prompt

# Declara modelo llm
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.5)

# Reyriever se usa para recuperar el contexto relacionado con la pregunta
retriever = vectorstore.as_retriever()

retrieval_chain = (
    {"context": retriever,  "question": RunnablePassthrough()}
    |  prompt 
    |  llm
    |  StrOutputParser() 
    )


question = "busca la pagina pagina mio.html" 

respuesta = retrieval_chain.invoke(question)

print(respuesta)