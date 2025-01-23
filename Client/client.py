from socket import socket, AF_INET, SOCK_STREAM
import logging
from threading import Thread
import argparse
import json

HOST = "server"
PORT = 4333

message = {
    "type": "OperationType",
    "data": {}
}

session = {
    "ID": -0,
    "User": "#"
}

user_data = {
    "ID": 0,
    "UserName": "a",
    "GamesList": {}
}

class ChatClient:
    def __init__(self, host, port):
        self.logger = self._setup_logger()
        self.sock = self._setup_socket(host, port)

        self.start_comms()

    # Enviar mensaje y recibir respuesta del servidor
    def manage_comms(self, encoded_data):
        self.sock.send(encoded_data)
        server_response = self.sock.recv(1024)
        decoded_response = json.loads(server_response.decode("utf-8"))

        if decoded_response["type"] == "LOGIN_RES": # Respuesta de inicio de sesion
            session["ID"] = decoded_response["data"]["ID"]
            session["User"] = decoded_response["data"]["User"]

            print("Sesión iniciada")
        elif decoded_response["type"] == "NEW_USR_RES": # Respuesta de registro de usuario
            session["ID"] = decoded_response["data"]["ID"]
            session["User"] = decoded_response["data"]["User"]

            print("Usuario creado, iniciando sesión")
        elif decoded_response["type"] == "GAMES_LIST_RES": # Respuesta de compra de juego
            games_res = decoded_response["data"]
            games_str = json.dumps(games_res, indent=4)

            print(games_str)
            inpt = input("ID de juego: ")

            game_selection = {
                "Game_ID": inpt
            }

            message["type"] = "GAME_SELECTION"
            message["data"] = game_selection

            response = json.dumps(message).encode("utf-8")

            self.manage_comms(response)
        elif decoded_response["type"] == "NEW_GAME_RES": # Respuesta con el juego comprado
            new_game = decoded_response["data"]
            user_data["GamesList"] = new_game

            print(new_game["Name"] + " ha sido añadido a la biblioteca")
        elif decoded_response["type"] == "USER_GAMES_LIST_RES": # Respuesta de juegos del usuario
            game_list = decoded_response["data"]
            game_list_str = json.dumps(game_list, indent=4)
            print("Juegos disponibles:")
            print(game_list_str)
        elif decoded_response["type"] == "EDIT_PASSWORD_RES": # Respuesta de cambio de contraseña
            if decoded_response["data"]["Status"] == "Success":
                print(decoded_response["data"]["Message"])
            else:
                print(decoded_response["data"]["Message"])
        elif decoded_response["type"] == "EDIT_USERNAME_RES": # Respuesta de cambio de username
            session["User"] = decoded_response["data"]["NewUsername"]
            user_data["UserName"] = decoded_response["data"]["NewUsername"]

            print(decoded_response["data"]["Message"])
        elif decoded_response["type"] == "LOGOUT_RES":
            session["ID"] = decoded_response["data"]["ID"]
            session["User"] = decoded_response["data"]["User"]

            print("Sesion terminada")

    # Acciones del usuario
    def select_operation(self, user_op):
        if user_op == "1" and session["ID"] == -0:
            self.login()
        elif user_op == "2" and session["ID"] == -0:
            self.sign_up()
        elif user_op == "1" and session["ID"] != -0:
            self.purchase_game()
        elif user_op == "2" and session["ID"] != -0:
            self.user_games_list()
        elif user_op == "3" and session["ID"] != -0:
            self.edit_username()
        elif user_op == "4" and session["ID"] != -0:
            self.edit_user_password()
        elif user_op == "5" and session["ID"] != -0:
            self.logout()
            
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
    def purchase_game(self):
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

    # Lista de juegos del usuario
    def user_games_list(self):
        message = {
            "type": "USER_GAMES_LIST",
            "data": {}
        }

        response = json.dumps(message).encode("utf-8")

        self.manage_comms(response)

    # Editar contraseña
    def edit_user_password(self):
        print("Para cambiar su contraseña primero debe introducir su contraseña actual")
        old_password = input("Contraseña actual: ")
        new_password = input("Nueva contraseña: ")

        user_password = {
            "User_ID": session["ID"],
            "OldPassword": old_password,
            "NewPassword": new_password
        }

        message["type"] = "EDIT_PASSWORD"
        message["data"] = user_password

        response = json.dumps(message).encode("utf-8")

        self.manage_comms(response)

    # Editar nombre de usuario
    def edit_username(self):
        new_username = input("Proporcione un nuevo nombre de usuario: ")

        message = {
            "type": "EDIT_USERNAME",
            "data" : new_username
        }

        response = json.dumps(message).encode("utf-8")

        self.manage_comms(response)

    # Cerrar sesion
    def logout(self):
        message = {
            "type": "LOGOUT",
            "data": {
                "User_ID": 1
            }
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
                3.- Editar nombre de usuario
                4.- Cambiar contraseña
                5.- Cerrar sesión
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
    client = ChatClient(HOST, PORT)