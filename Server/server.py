from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import logging
from concurrent.futures import ThreadPoolExecutor
import datetime

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
                a = str("(" + addr[0] + " | ").encode('utf-8')
                now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
                now += ") "
                now = now.encode('utf-8')
                connection.send(a + now + data)

            if not data:
                self.logger.warning("No se han recibido datos. Terminando proceso.")
                break

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