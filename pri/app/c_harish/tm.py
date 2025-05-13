from typing import Annotated, TypedDict

# Esta función actuará como "metadato", decorador o marcador
def add_messages(messages: list) -> list:
    messages.append("Mensaje inicial del sistema")
    return messages

# TypedDict con Annotated
class ChildState(TypedDict):
    messages: Annotated[list, add_messages]

# Función que simula la creación del estado del agente
def create_child_state() -> ChildState:
    raw_messages = []
    
    # Accedemos al tipo anotado y ejecutamos la función `add_messages`
    annotated_type = ChildState.__annotations__['messages']
    
    # Extraemos la función `add_messages` del tipo Annotated
    base_type, metadata_fn = annotated_type.__origin__, annotated_type.__metadata__[0]

    # Aplicamos el decorador a los mensajes
    messages = metadata_fn(raw_messages)
    
    return ChildState(messages=messages)

# Ejecutamos
estado = create_child_state()
print(estado)
