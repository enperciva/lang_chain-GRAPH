# Librerias para interactuar con el entorno
import os
import warnings
warnings.filterwarnings("ignore")
from dotenv import load_dotenv, find_dotenv 
import random 


# pip para accesar los embeddings en pinecone
from pinecone import Pinecone

load_dotenv(find_dotenv(), override=True)

""" 
# ==================================================================
# Trabajando con indices en Pinecone
# ==================================================================

# Para instanciar en langchain los indices creados en la plataforma Pinecone
pc = Pinecone()

# Lista los indices creados en la plataforma
pc.list_indexes()

# Imprime los detalles de un determinado indice
pc.describe_index("xdenprueba")

# Elimina determinado indice
pc.delete_index("xdenprueba")

# Crear un nuevo indice 
# Hay que importar antes esta libreria  "" from pinecone import PopSpec ""

pc.create_index( 
    name=index_name, 
    dimension=3072, 
    metric='cosine', 
    spec PodSpec( 
    environment="gcp-starter' 
            ) 
)

# ==================================================================
# Trabajando Vecetores en pipecone
# ==================================================================

 """


import random 
vectores = [[random.random() for _ in range(3072)] for v in range(5)]

for vector in vectores:
    print(vector) 

# Creando vectores la estructura se veria asi :
""" 
vectores (lista de 5 vectores)
├── vector_1: [x1, x2, ..., x3072]
├── vector_2: [x1, x2, ..., x3072]
├── vector_3: [x1, x2, ..., x3072]
├── vector_4: [x1, x2, ..., x3072]
└── vector_5: [x1, x2, ..., x3072]
 """

# Agregando ids la estructura del indice se veria asi :
 ids = ['abcde']

"""  
vectores (lista de 5 vectores)
├── vector_1
│   ├── id: "vec_01"
│   └── values: [x1, x2, ..., x3072]
├── vector_2
│   ├── id: "vec_02"
│   └── values: [x1, x2, ..., x3072]
├── vector_3
│   ├── id: "vec_03"
│   └── values: [x1, x2, ..., x3072]
├── vector_4
│   ├── id: "vec_04"
│   └── values: [x1, x2, ..., x3072]
└── vector_5
    ├── id: "vec_05"
    └── values: [x1, x2, ..., x3072]
     """

# Agregando los ids a los vectores dentro del indice
index_name = 'langchain' 
index = pc.Index(index_name) 
index.upsert(vectors=zip(ids, vectors))


# Para mostrar los vectores de los ids 'c' y 'd'
index.fetch(ids['c','d'])

# Para elindex.fetch(ids['c','d'])
index.delete(ids['c','d'])

# Para ver las modificaciones que vas haciendo con la estructura del indice
index.describe_index_stats()

# Creando un vector aleatorio
vectores = [random.random() for _ in range(3072)] 

#Para hacer queries dentro de los indices

vectores = [random.random() for _ in range(3072)] 

index.query( 
    vector = vectores, 
    top_k=3, 
    include_values=False 
) 

# Resultado :
{'matches': [{'id': 'c', 'score': 0.869315, 'values': [ 
             ('id': 'd', 'score': 0.761867166, 'values': []}, 
             ('id': 'b', 'score': 0.753967941, 'values': []}], 
'namespace': '', 
'usage': {'read_units': 5}}

