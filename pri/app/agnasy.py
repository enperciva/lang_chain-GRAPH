# Librerias del ambiente de entorno 
import os
import warnings
warnings.filterwarnings("ignore")
from dotenv import load_dotenv, find_dotenv 

import asyncio 
from agents import Agent, Runner, function_tool 
load_dotenv() 


@function_tool 
def get_weather(city: str) -> str: 
    # run api call 
    #connect db 
    return f"The weather in {city} is sunny" 

agent = Agent ( 
    name = "Haiku agent", 
    instructions="Always respond in haiku form", 
    model = "03-mini", 
    tools=[get_weather]
)
    

async def main(): 
    msg = input("Hola, como puedo ayudarte? ") 
    result = await Runner.run(agent, msg) 
    print('Respuesta: ', result.final_output) 


if __name__ == _main__: 
    asyncio.run(main())