from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import logging
from concurrent.futures import ThreadPoolExecutor
import datetime
import json

response = {
    "type": "OperationType",
    "data": {}
}

class ChatServer:
    def __init__(self, host, port):
        self.logger = self._setup_logger()
        self.sock = self._setup_socket(host, port)
        self.connections = []

    def run(self):
        self.logger.info("El servidor esta activo")

        with ThreadPoolExecutor() as executor:
            while True:
                #Bloquear y esperar conexiones nuevas
                #regresa una tupla que contiene un nuevo objeto socket
                #con la conexion y direccion del cliente
                conn, addr = self.sock.accept()
                self.logger.debug(f"Nueva conexion: {addr}")

                self.connections.append(conn)
                self.logger.debug(f"Conexiones: {self.connections}")

                executor.submit(self.relay_messages, conn, addr)

    def relay_messages(self, conn, addr):
        while True:
            data = conn.recv(4096)

            for connection in self.connections:
                # Decodificar datos
                msg = json.loads(data.decode("utf-8"))
                self.logger.debug("Datos recibidos")

                # Manejar datos y respuesta
                connection.send(self.handle_messages(msg, addr))

            if not data:
                self.logger.warning("No se han recibido datos. Terminando proceso.")
                break

    # Recibir mensaje y procesar operacion
    def handle_messages(self, data, addr):
        message = data
        if (message["type"] == "LOGIN"):
            return self.login()
        elif (message["type"] == "NEW_USR"):
            return self.create_user()
        elif (message["type"] == "GAMES_LIST"):
            return self.games_list()

    # Inicio de sesion
    def login(self):
        self.logger.debug("Inicio de sesión")
        
        session = {
            "ID": 1,
            "User": "Alejandro"
        }

        response["type"] = "LOGIN_RES"
        response["data"] = session

        server_response = json.dumps(response).encode("utf-8")

        return server_response

    # Crear nuevo usuario
    def create_user(self):
        self.logger.debug("Registrar nuevo usuario")

        session = {
            "ID": 2,
            "User": "Salvador"
        }

        response["type"] = "NEW_USR_RES"
        response["data"] = session

        server_response = json.dumps(response).encode("utf-8")

        return server_response

    # Agregar juego nuevo a cuenta de usuario
    def pruchase_game(self):
        self.logger.debug("Compra de juego")

        game_data = {
            "ID": 1,
            "Name": "Juego chingón",
            "Genre": "Plomazos"
        }

        response["type"] = "NEW_GAME"
        response["data"] = game_data

        server_response = json.dumps(response).encode("utf-8")

        return server_response

    # Lista de juegos disponibles
    def games_list(self):
        self.logger.debug("Lista de juegos")

        games = [
            {
                "ID": 1,
                "Name": "Juego chingón",
                "Genre": "Plomazos"
            },
            {
                "ID": 2,
                "Name": "Juego A",
                "Genre": "A"
            },
            {
                "ID": 3,
                "Name": "Juego B",
                "Genre": "B"
            },
            {
                "ID": 4,
                "Name": "Juego C",
                "Genre": "C"
            }
        ]

        response["type"] = "GAMES_LIST_RES"
        response["data"] = games

        server_response = json.dumps(response).encode("utf-8")

        return server_response

    @staticmethod
    def _setup_socket(host, port):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        sock.bind((host, port))
        sock.listen()
        return sock

    @staticmethod
    def _setup_logger():
        logger = logging.getLogger('chat_server')
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.DEBUG)
        return logger

if __name__ == "__main__":
    server = ChatServer('localhost', 4333)
    server.run()