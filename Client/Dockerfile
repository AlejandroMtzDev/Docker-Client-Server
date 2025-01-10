# Se importa la imagen base del proyecto desde DockerHub
# En este caso la version mas reciente de python
FROM python:latest

ADD client.py /client/

# El comando workdir cambia el directorio base de la imagen de Docker
# En este caso se define '/client/' como el directorio base desde donde se ejecutaran todos los comandos
WORKDIR /client/