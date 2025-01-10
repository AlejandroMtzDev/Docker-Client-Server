# Se importa la imagen base del proyecto desde DockerHub
# En este caso la version mas reciente de python
FROM python:latest

ADD server.py /server/

# El comando workdir cambia el directorio base de la imagen de Docker
# En este caso se define '/server/' como el directorio base desde donde se ejecutaran todos los comandos
WORKDIR /server/