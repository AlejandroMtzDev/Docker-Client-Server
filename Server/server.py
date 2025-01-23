from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import logging
from concurrent.futures import ThreadPoolExecutor
import json

HOST = "0.0.0.0"
PORT = 4333

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
                connection.send(self.handle_messages(msg))

            if not data:
                self.logger.warning("No se han recibido datos. Terminando proceso.")
                break

    # Recibir mensaje y procesar operacion
    def handle_messages(self, data):
        message = data
        if (message["type"] == "LOGIN"):
            return self.login()
        elif (message["type"] == "NEW_USR"):
            return self.create_user()
        elif (message["type"] == "GAMES_LIST"):
            return self.games_list()
        elif (message["type"] == "GAME_SELECTION"): # Proceso para comprar un juego            
            id = message["data"]["Game_ID"]
            return self.game_purchase(id)
        elif (message["type"] == "USER_GAMES_LIST"):
            return self.user_games_list()
        elif (message["type"] == "EDIT_PASSWORD"):
            return self.edit_user_password(message["data"])
        elif (message["type"] == "EDIT_USERNAME"):
            return self.edit_username(message["data"])
        elif (message["type"] == "LOGOUT"):
            return self.logout()
        else:
            return "Operación inválida"

    # Inicio de sesion
    def login(self):
        self.logger.debug("Inicio de sesión")
        
        # Despues de recibir los datos del usuario y procesar los 
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
    def game_purchase(self, id):
        self.logger.debug("Compra de juego")

        games = [
            {
                "ID": 1,
                "Name": "Juego A",
                "Genre": "Genero A"
            },
            {
                "ID": 2,
                "Name": "Juego B",
                "Genre": "Genero B"
            },
            {
                "ID": 3,
                "Name": "Juego C",
                "Genre": "Genero C"
            },
            {
                "ID": 4,
                "Name": "Juego D",
                "Genre": "Genero D"
            }
        ]

        game_data = {
            "ID": 0,
            "Name": "a",
            "Genre": "b"
        }

        for x in games:
            if x["ID"] == int(id):
                game_data["ID"] = x["ID"]
                game_data["Name"] = x["Name"]
                game_data["Genre"] = x["Genre"]

        response["type"] = "NEW_GAME_RES"
        response["data"] = game_data

        server_response = json.dumps(response).encode("utf-8")

        return server_response

    # Lista de juegos disponibles
    def games_list(self):
        self.logger.debug("Lista de juegos")

        games = [
            {
                "ID": 1,
                "Name": "Juego A",
                "Genre": "A"
            },
            {
                "ID": 2,
                "Name": "Juego B",
                "Genre": "B"
            },
            {
                "ID": 3,
                "Name": "Juego C",
                "Genre": "C"
            },
            {
                "ID": 4,
                "Name": "Juego D",
                "Genre": "D"
            }
        ]

        response["type"] = "GAMES_LIST_RES"
        response["data"] = games

        server_response = json.dumps(response).encode("utf-8")

        return server_response
    
    # Peticion para obtener los juegos del usuario
    def user_games_list(self):
        self.logger.debug("Juegos del usuario")

        user_games = [
            {
                "ID": 1,
                "Name": "Juego A",
                "Genre": "A"
            },
            {
                "ID": 2,
                "Name": "Juego B",
                "Genre": "B"
            }
        ]

        response["type"] = "USER_GAMES_LIST_RES"
        response["data"] = user_games

        server_response = json.dumps(response).encode("utf-8")

        return server_response

    # Cambio de contraseña
    def edit_user_password(self, data):
        self.logger.debug("Cambio de contaseña")

        # Objeto que ilustra un usuario en la base de datos
        user_data = {
            "User_ID": 1,
            "UserName": "Alejandro",
            "Password": "Psswrd"
        }

        # Objeto que servira para notificar al usuario el resultado de su operacion
        op_response = {
            "Status": "a",
            "Message": "b"
        }

        # El servidor procesa la operacion del usuario y si determina que la contraseña
        # coincide con aquella almacenada en la "base de datos" envia un mensaje al usuario
        # notificandole si su solicitud tuvo exito o no
        if data["OldPassword"] == user_data["Password"]:
            op_response["Status"] = "Success"
            op_response["Message"] = "Su contraseña ha sido cambiada con éxito"
        else:
            op_response["Status"] = "Failure"
            op_response["Message"] = "Las contraseñas no coinciden, intente otra vez"

        response["type"] = "EDIT_PASSWORD_RES"
        response["data"] = op_response

        server_response = json.dumps(response).encode("utf-8")

        return server_response

    # Cambio de username
    def edit_username(self, data):
        self.logger.debug("Cambio de nombre de usuario")

        # Objeto que ilustra un usuario en la base de datos
        user_data = {
            "User_ID": 1,
            "UserName": "Alejandro",
            "Password": "Psswrd"
        }

        op_response = {
            "NewUsername": data,
            "Message": "Nombre de usuario actualizado con éxito"
        }

        # El servidor cambia el username del usuario en la "base de datos"
        user_data["UserName"] = data

        response["type"] = "EDIT_USERNAME_RES"
        response["data"] = op_response

        server_response = json.dumps(response).encode("utf-8")

        return server_response

    # Cerrar sesion
    def logout(self):
        self.logger.debug("Cerrar sesion de usuario")

        # El servidor recibe la solicitud del usuario y manda una respuesta
        session = {
            "ID": -0,
            "User": "#"
        }

        response["type"] = "LOGOUT_RES"
        response["data"] = session

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
    server = ChatServer(HOST, PORT)
    server.run()