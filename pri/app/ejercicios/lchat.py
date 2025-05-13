import os
from  dotenv import load_dotenv
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from lchat_cargadata import cargar_documentos, crear_vectorstore
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_community.llms import HuggingFaceHub
from langchain_google_genai import ChatGoogleGenerativeAI
import warnings

warnings.filterwarnings("ignore")

load_dotenv()


# Códigos de escape ANSI para colores
AZUL = "\033[94m"
VERDE = "\033[92m"
RESET = "\033[0m"

#os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv("HUGFACE_TOKEN")
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

def iniciar_chat(ruta_archivo):


    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.1)


    #embed_model = FastEmbedEmbeddings(model_name="text-embedding-005")
    embed_model = OllamaEmbeddings(model="nomic-embed-text")   

    vectorstore = Chroma(embedding_function=embed_model,
                                       persist_directory="chroma_db_dir2",
                                       collection_name="stanford_report_data")

    total_rows = len(vectorstore.get()['ids'])
    
    if total_rows == 0:
        docs = cargar_documentos(ruta_archivo)
        vectorstore = crear_vectorstore(docs)
    retriever = vectorstore.as_retriever(search_kwargs={'k': 1})

    custom_prompt_template = """ Tienes un documento cargado en la vectorestore. Ese documento habla sobre la vida de Enmanuel Kant.
    responde las preguntas que te hagan sobre el. solo utiliza los datos que tienes almacenados en la vectorstore.

    Context: {context}
    Question: {question}

    Only return the helpful answer below and nothing else but in spanish.
    Helpful answer:
    """
    prompt = PromptTemplate(template=custom_prompt_template, input_variables=['context', 'question'])

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=False,
        chain_type_kwargs={"prompt": prompt}
    )

    print("¡Bienvenido al chat! Escribe 'salir' para terminar.")
    while True:
        pregunta = input(f"{AZUL}Tú:{RESET} ")
        if pregunta.lower() == 'salir':
            print("¡Hasta luego!")
            break

        respuesta = qa.invoke({"query": pregunta})
        print(respuesta)
        metadata = []
        """ for _ in respuesta['source_documents']:
            metadata.append(('page_content'+str(_.metadata['page_content']), _.metadata['file_path'])) 
        print(f"{VERDE}Asistente:{RESET}", respuesta['result'], '\n', metadata)  """

if __name__ == "__main__":
    ruta_archivo = "C:\Box\\flowise\\datos\\benjamin\\Hitler.docx"
    iniciar_chat(ruta_archivo)