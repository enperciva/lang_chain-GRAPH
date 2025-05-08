Instalacion fundamental :

1.instalar vscode     https://code.visualstudio.com/download
2.instalar python     https://www.python.org/downloads/
3.Descargar e instalar conda (manejador de ambiente) https://www.anaconda.com/docs/main
4.crear archivos .env o contenedor de variables de ambiente 
   conda create -n nombre python=3.11
   
5.Instalar un gestor de dependencias.  Este comando instala poetry desde el canal de repositorios de librerias    
  llamado forge-poetry

      (conda install -c forge-poetry poetry)

6. Hacer un contenedor del repositorio de manera que si tengo que recrear el ambiente de trabajo para que se ejecute mi proyecto, solo tenga que restaurar el ambiente guardado. se guarda con el comando :

      conda env export -- from-history > mientorno.yml


7. Iniciar poetry para el manejo de las dependencias

      poetry init

Esto genera un archivo extension .toml que contiene datos generales del proyectos
asi como de las dependencias de recursos de librerias del mismo.

8. Instalar un debugger de langgraph

   poetry add  "langgraph-cli[inmem]

9. Crear archivo json langgraph.json
   Los datos de este archivo los utiliza langsmith para realizar el debuging de la ejecucion del agente.

9. Es el comando para llamar el debbuguer :

      langgraph dev

10.Instalar fastapi. Fastapi hace el despliegue del agente en un ambiente web

      poetry add "fastapi[standard]"

      crear archivo api.py

       En ese archivo api.py ira el codigo necesario para el despliegue :

11. Para desplegar finalmente el agente en el endpoint :

      fastapi dev app/api.py 



nota : instalar la extension de vscode 'continue'. para utilizar AI dentro del editor y solicitarle codigo.

Create environment from scratch
conda create -n agents python=3.11
conda activate agents
conda install -c conda-forge poetry
conda env export --from-history > environment.yml
Create environment from file
conda env create -f environment.yml
Run agent
langgraph dev
Run fastapi server
fastapi dev app/api.py
