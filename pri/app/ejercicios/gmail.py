# Para tener control del flujo del grafo
from langgraph.graph import StateGraph, END

# Libreria de herramientas
from langchain.tools import tool

# Libreria que administra y activa las credenciales de acceso a los servicios de google
from google.oauth2.credentials import Credentials

# Manea el flujo de autenticación desde la aplicacion al cliente OAuth 2.0, a partir de los datos del credentials.json 
from google_auth_oauthlib.flow import InstalledAppFlow

# La encargada de crear un cliente para interactuar con una API de Google
from googleapiclient.discovery import build

# Interviene en el contenido o cuerpo del correo(texto, destinatarios y recipiente, metadados del texto,etc)
from email.mime.text import MIMEText

# Para codificar y decodificar datos usando el formato Base64, que es el que utiliza gmail en sus correos
import base64
import os
from dataclasses import dataclass
import json

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/gmail.send']

def autenticar_gmail():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
        creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return build("gmail", "v1", credentials=creds)

servicio_gmail = autenticar_gmail()


#===================================================================================
# Comprobar si se autentico en gmail correctamente
#===================================================================================
""" with open("token.json", "r") as f:
    data = json.load(f)
    print("Token obtenido para:", data.get("client_id", "desconocido")) """

perfil = servicio_gmail.users().getProfile(userId='me').execute()
print("Autenticado como:", perfil["emailAddress"])

# Estado que se pasa entre nodos
""" class GmailState(dict):
    pass """

@dataclass
class GmailState:
    destinatario: str = ""
    asunto: str = ""
    cuerpo: str = "" 
    correos: list = None
    correo_enviado: bool = False

@tool
def leer_ultimos_correos(state: GmailState) -> GmailState:

    """ Esta funcion se encarga de leer los 3 ultimos correos del buzon """ 


    print("📥 Leyendo correos...")
    resultados = servicio_gmail.users().messages().list(userId='me', maxResults=3).execute()
    mensajes = resultados.get('messages', [])
    resumen = []

    for mensaje in mensajes:
        msg = servicio_gmail.users().messages().get(userId='me', id=mensaje['id']).execute()
        asunto = next((h['value'] for h in msg['payload']['headers'] if h['name'] == 'Subject'), '(Sin asunto)')
        resumen.append(asunto)

    print("✅ Correos leídos:")
    for i, s in enumerate(resumen, 1):
        print(f"{i}. {s}")


    state["correos"] = resumen
    return state

@tool
def enviar_correo(state: GmailState) -> GmailState:

    """ Esta funcion se encarga de enviar un correo a la cuenta especificada """ 

    print("✉️ Enviando correo...")

    destinatario = "enperciva@gmail.com"  # <- CAMBIA ESTO
    asunto = "Correo automático desde LangGraph"
    cuerpo = "Este mensaje fue enviado por un agente LangGraph con integración Gmail."
    
    state["destinatario"] = destinatario
    state["asunto"] = asunto
    state["cuerpo"] = cuerpo

    mensaje = MIMEText(cuerpo)
    mensaje["to"] = destinatario
    mensaje["subject"] = asunto
    mensaje_bytes = base64.urlsafe_b64encode(mensaje.as_bytes()).decode()

    enviado = servicio_gmail.users().messages().send(
        userId="me", body={"raw": mensaje_bytes}).execute()

    print(f"✅ Correo enviado. ID: {enviado['id']}")
    state["correo_enviado"] = True
    return state

# Construcción del grafo
builder = StateGraph(GmailState)
builder.add_node("leer", leer_ultimos_correos)
builder.add_node("enviar", enviar_correo)

builder.set_entry_point("enviar")
builder.add_edge("enviar", "leer")
builder.add_edge("leer", END)

grafo = builder.compile()

# Ejecutar
estado_inicial = GmailState()

estado_inicial = {GmailState.destinatario: "enperciva@gmail.com", GmailState.asunto:"Correo automático desde LangGraph", GmailState.cuerpo: "Este mensaje fue enviado por un agente LangGraph con integración Gmail." }
print(estado_inicial)
final = grafo.invoke(estado_inicial)
