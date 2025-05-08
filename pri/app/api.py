from fastapi import FastAPI
from agent import graph

app = FastAPI()


@app.get("/")
def agent():
    return graph.invoke({"customer_name" : "John" ,  "my_var" :"Hello"   })

