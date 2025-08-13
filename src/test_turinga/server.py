from socket import socket, AF_INET, SOCK_STREAM
import threading
from random import choice
import logging
from typing import Sequence

from .handlers import MessageHandler

logger = logging.getLogger(__name__)

RECV_BUFFER_SIZE = 1024


class Server:
    def __init__(self, handlers: Sequence[MessageHandler]):
        if len(handlers) == 0:
            raise ValueError("At least one handler must be provided")
        self.handlers = handlers
        logger.info("Server initialized")

    def main(self, host: str, port: int) -> None:
        main_socket = socket(AF_INET, SOCK_STREAM)
        main_socket.bind((host, port))
        main_socket.listen()
        logger.debug(f"Server started on {host}:{port}")

        while True:
            client_socket, addr = main_socket.accept()
            logger.info(f"Accepted connection from {addr}")
            threading.Thread(target=self.handle, args=(client_socket,)).start()

    def handle(self, client_socket: socket) -> None:
        handler = choice(self.handlers)
        handler.handle(client_socket)
