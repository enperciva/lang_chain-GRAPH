from langchain.chains import SimpleSequentialChain
import os
from  dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.chains import LLMChain
import warnings

warnings.filterwarnings("ignore")
load_dotenv()

os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

llm = ChatGoogleGenerativeAI(model = "gemini-2.0-flash" , temperature=0.1)

template1 = "detecta su el mensaje del cliente tiene sentido negativo o positivo {mensaje}"
PromptTemplate1 = ChatPromptTemplate.from_template(template=template1)
#chainmensaje1 =  PromptTemplate1 | llm
chainmensaje1 = LLMChain(llm=llm, prompt=PromptTemplate1)


template2 = "si el mensaje anterior tiene sentido negativo, da una disculpa y agradecimiento {messanterior}"
PromptTemplate2 = ChatPromptTemplate.from_template(template=template2)
#chainmensaje2 =  PromptTemplate2 | llm

chainmensaje2 = LLMChain(llm=llm, prompt=PromptTemplate2)

#impresion = input("diga : ")


cadenach = SimpleSequentialChain(chains=[chainmensaje1, chainmensaje2 ])

respuesta = cadenach.invoke("la caja llego sucia")

print(respuesta)

