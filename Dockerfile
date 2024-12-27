#----- Imagen base de prefect 
FROM prefecthq/prefect:2.10.13-python3.8

WORKDIR /opt/prefect

#----- Instalando netcat para poder validar
RUN apt-get update && apt-get install -y netcat

#----- Instalando requirements y pytest
COPY requirements.txt .
RUN pip install -r requirements.txt

RUN pip install pytest

COPY . .

#----- Iniciando el script de ejecucion de prefect
RUN chmod +x start.sh

ENTRYPOINT ["bash", "./start.sh"]
