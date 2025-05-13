from langchain.chains import SequentialChain
from  dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import LLMChain
import warnings
import os

warnings.filterwarnings("ignore")
load_dotenv()

os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

llm = ChatGoogleGenerativeAI(model = "gemini-2.0-flash" , temperature=0.1)

# cadena 01 | input: reseña | output: spanish_rev
one_template = ChatPromptTemplate.from_template("""
Traducir la siguiente reseña en español {review}
""")
chain_one = LLMChain(llm=llm, prompt=one_template, output_key="spanish_rev")

# Cadena 02 | input spanish_rev | output resumen
two_template = ChatPromptTemplate.from_template("""
resume la siguiente reseña en una frase {spanish_rev}
""")
chain_two = LLMChain(llm=llm, prompt=two_template, output_key="resumen")

#cadena 03 | input review | output lenguaje
three_template = ChatPromptTemplate.from_template("""
En que idioma se encuentra la siguiente reseña {review}
""")
chain_three = LLMChain(llm=llm, prompt=three_template, output_key="lenguaje")

#cadena 04 | input resumen,lenguaje | output mensaje_seg
four_template = ChatPromptTemplate.from_template("""
Escribe una respuesta de seguimiento a el siguiente resumen en el idioma especificado {resumen}, idioma: {lenguaje}
""")
chain_four = LLMChain(llm=llm, prompt=four_template, output_key="mensaje_seg")

#flujo de cadena

cadena_secuencial = SequentialChain(
    chains=[chain_one, chain_two, chain_three, chain_four],
    input_variables=["review"],
    output_variables=["spanish_rev", "resumen", "lenguaje", "mensaje_seg"]
)
     

review = """For all their convenience, Bluetooth headphones and earbuds have fundamental problems.
            Take their batteries (please). They're only fully rechargeable 300–500 times,
            which means that after just two or three years of moderate-to-heavy use,
            most people toss their depleted wireless ear-fi in a drawer and buy a new pair."""
     

result = cadena_secuencial.invoke(review)
     

print("Traduccion: "+ result['spanish_rev'] +"\n\n"+
      "Resumen: "+ result['resumen'] +"\n\n"+
      "Idioma: "+ result['lenguaje'] +"\n\n"+
      "Respuesta: "+ result['mensaje_seg']
      )
     