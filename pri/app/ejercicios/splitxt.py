#===================================================================
#Splitting y Embedding textos usando LangChain (Similarity Search) 
#===================================================================

# Librerias para interactuar con el entorno
import os
import warnings
warnings.filterwarnings("ignore")
#cargar variables de entorno desde un archivo 
from dotenv import load_dotenv, find_dotenv 

# Declarando las librerias que haran la funciones de cargar y segmentar el texto del documento pdf
from langchain.text_splitter import RecursiveCharacterTextSplitter 
from langchain.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain_community.document_loaders import PyMuPDFLoader

# Declarando las librerias que haran la funciones de cargar y segmentar el texto del documento docx


# Libreria necesaria para utilizar el metodo de embedding nomic-embed-text
from langchain_community.embeddings import HuggingFaceEmbeddings

# Libreria de embedding FastEmbedEmbeddings
import pinecone 
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings

# Librerias de pinecone
from langchain_community.vectorstores import Pinecone 
from pinecone import PodSpec 

# libreria de vectores 
from langchain_community.vectorstores import Chroma

# Libreria de prompts de langchain 
from langchain.prompts import PromptTemplate

# Libreria del llm a utilizar 
from langchain_google_genai import ChatGoogleGenerativeAI

# Libreria del chain y chain retrievers a utilizar 
from langchain.chains import LLMChain
from langchain.chains import RetrievalQA

load_dotenv()

#os.environ["PINECONE_API_KEY"] = os.getenv("PINECONE_API_KEY")

# Credenciales de api del llm de google 
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

# Declara modelo llm
llm = ChatGoogleGenerativeAI(model = "gemini-2.0-flash" , temperature=0.5)

# Cargar el PDF
#loader = PyMuPDFLoader("bsebo.pdf") 
loader = Docx2txtLoader("bsebo.docx") 

texto_completo = loader.load() 


# Unir todo el contenido en un solo texto (si quieres procesarlo como un único documento)
#texto_completo = "\n".join([p.page_content for p in pages])

""" #Carga el documento en memoria
with open('100.txt', encoding='utf-8') as f:
    ggm = f.read() 
 """


# Define como se va a segmentar el texto    
segmentador = RecursiveCharacterTextSplitter(
    chunk_size=500,       # Puedes ajustar este tamaño
    chunk_overlap=80,     # Cuánto se superpone cada chunk
    length_function=len
)

# Se crean los chunks 
chunks = segmentador.split_documents(texto_completo)

print(len(chunks))


#===================================================================================
#Definir Embedding 
#===================================================================================


modelo_embedding = FastEmbedEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=modelo_embedding,
        persist_directory="C:\\Box\\flowise\datos\\ggm",
        collection_name="stanford_report_data"
    )
#===================================================================================
#Crear vector 
#===================================================================================
#vector = modelo_embedding.embed_query(chunks[0]) 

#print(vector)
#===================================================================================
# Una vez creados los vectores procedemos a crear los indices de esos vectores en pinecone
#===================================================================================

# Instanciar comunicacion con la plataforma pinecone
""" #pc = pinecone. Pinecone() 

# Antes de todo, se eliminan los indices que actualmente estan creados en pinecone
indexes = pc.list_indexes().names() 
for i in indexes: 
    print('Borrando los indices...', end='') 
    pc.delete_index(i) 
    print('Listo..')


# nombre del nuevo indice a crear
index_name = 'oscarproj' 

# Se procede a crear dentro de pinecone el nuevo indice para los vectores 
if index_name not in pc.list_indexes().names():
    print(f'Creando el indice {index_name}') 
    pc.create_index( 
        name=index_name, 
        dimension=3072, 
        metric='cosine', 
        spec = PodSpec(environment='us-east-1-aws') 
    ) 
    print('Indice Creado') 
else: 
    print(f"indice {index_name} ya existe")

# Se cargan en la plataforma de pinecone los vectores dentro del indice creado
vector_store = Pinecone.from_documents(chunks, embeddings, index_name=index_name) 

# Se procede a verificar las = estadisticas de carga de los vectores al indice
index = pc.Index(index_name) 
index.describe_index_stats()  """





#===================================================================================
# Vamos autilizar un prompttemplate para hacer busquedas en el vector store
#===================================================================================


#Declarar prompt template
template = """tienes cargado el cuento Bola de Sebo dentro de un vector store.
            debes responder todas las preguntas que te hagan en relacion al cuento.  
            En la respuesta no debe ir el texto de contexto de la pregunta.
            contexto : {context}
            questions : {question}
            """

prompt_template = PromptTemplate(template=template, input_variables=["context","question"])
                        
#chain = LLMChain(llm=llm, prompt=prompt_template )
#chain = prompt_template | llm

retriever = vector_store.as_retriever(search_kwargs={'k': 1})

chain_r = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=False,
    chain_type_kwargs={"prompt": prompt_template}
)






# Realizando preguntas (utilizando el metodo Similarity Search) 
pregunta = "quien era el conde de Breville ?" 
#resultado = vector_store.similarity_search(pregunta) 
resultado = chain_r.invoke({"query":pregunta})
print(resultado)