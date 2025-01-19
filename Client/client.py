from socket import socket, AF_INET, SOCK_STREAM
import logging
from threading import Thread
import argparse
import json

message = {
    "type": "OperationType",
    "data": {}
}

session = {
    "ID": -0,
    "User": "#"
}

class ChatClient:
    def __init__(self, host, port):
        self.logger = self._setup_logger()
        self.sock = self._setup_socket(host, port)

        self.start_comms()

    # Enviar mensaje y recibir respuesta del servidor
    def manage_comms(self, encoded_data):
        try:
            self.sock.send(encoded_data)
            server_response = self.sock.recv(1024)
            decoded_response = json.loads(server_response.decode("utf-8"))

            if decoded_response["type"] == "LOGIN_RES":
                session["ID"] = decoded_response["data"]["ID"]
                session["User"] = decoded_response["data"]["User"]

                print("Sesión iniciada")
            elif decoded_response["type"] == "NEW_USR_RES":
                session["ID"] = decoded_response["data"]["ID"]
                session["User"] = decoded_response["data"]["User"]

                print("Usuario creado, iniciando sesión")
            elif decoded_response["type"] == "GAMES_LIST_RES":
                games_res = decoded_response["data"]
                games_str = json.dumps(games_res, indent=4)

                print(games_str)
                inpt = input("ID de juego: ")

        except Exception as e:
            print(e)

    # Acciones del usuario
    def select_operation(self, user_op):
        if user_op == "1" and session["ID"] == -0:
            self.login()
        elif user_op == "2":
            self.sign_up()
        elif user_op == "1" and session["ID"] != -0:
            self.pruchase_game()
            
    # Inicio de sesion
    def login(self):
        print("Para iniciar sesión proporcione su usuario y contraseña")
        user = input("User: ")
        psswrd = input("Password: ")

        login_data = {
            "user": user,
            "password": psswrd
        }

        message["type"] = "LOGIN"
        message["data"] = login_data

        # Convertir diccionario a bytes para enviar mensaje al servidor
        response = json.dumps(message).encode("utf-8")

        self.manage_comms(response)

    # Registro de usuario
    def sign_up(self):
        print("Asigne un nombre de usuario y contraseña para su perfil")
        user = input("Nombre de usuario: ")
        psswrd = input("Contraseña: ")

        new_user_data = {
            "user": user,
            "password": psswrd
        }

        message["type"] = "NEW_USR"
        message["data"] = new_user_data

        response = json.dumps(message).encode("utf-8")

        self.manage_comms(response)

    # Agregar juego a perfil de usuario
    def pruchase_game(self):
        print("Para continuar con su compra seleccione un juego de la lista")
        self.games_list()

    # Ver juegos disponibles
    def games_list(self):
        message = {
            "type": "GAMES_LIST",
            "data": {}
        }

        response = json.dumps(message).encode("utf-8")

        self.manage_comms(response)

    # Muestra en consola las operaciones que el usuario puede hacer y envia la seleccion al servidor
    def start_comms(self):
        while True:

            if session["ID"] == -0 and session["User"] == "#":
                print('''
                === BIENVENIDO A GAMEACCOUNT. SELECCIONA UNA OPCIÓN PARA CONTINUAR ===
                1.- Iniciar sesión
                2.- Crear usuario
                ''')
                user_op = input("Selecciona el número de la operación: ")
            else:
                print(f'''
                === BIENVENIDO {session["User"]}. SELECCIONA UNA OPCIÓN PARA CONTINUAR ===
                1.- Comprar juego
                2.- Consultar lista de juegos
                3.- Consultar datos de un juego
                4.- Remover juego de biblioteca
                5.- Editar nombre de usuario
                6.- Cambiar contraseña
                7.- Cerrar sesión
                ''')
                user_op = input("Selecciona el número de la operación: ")

            self.select_operation(user_op)

    @staticmethod
    def _setup_socket(host, port):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect((host, port))
        return sock

    @staticmethod
    def _setup_logger():
        logger = logging.getLogger('chat_client')
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.DEBUG)
        return logger
    
if __name__ == "__main__":
    client = ChatClient('localhost', 4333)