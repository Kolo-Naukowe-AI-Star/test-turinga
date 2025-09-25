import logging
import socket
import threading
from random import choice
from collections.abc import Sequence
from .message import Message

from .handlers.base import MessageHandler

logger = logging.getLogger(__name__)

RECV_BUFFER_SIZE = 1024


class Server:
    def __init__(self, handlers: Sequence[MessageHandler]):
        if len(handlers) == 0:
            raise ValueError("At least one handler must be provided")
        self.handlers: Sequence[MessageHandler] = handlers
        logger.info("Server initialized")

    def main(self, host: str, port: int) -> None:
        main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        main_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        main_socket.bind((host, port))
        main_socket.listen()
        logger.debug(f"Server started on {host}:{port}")

        while True:
            client_socket, addr = main_socket.accept()
            logger.info(f"Accepted connection from {addr}")
            threading.Thread(target=self.handle, args=(client_socket,)).start()


    def handle(self, client_socket: socket.socket) -> None:
        while True:
            handler = choice(self.handlers)
            logger.info(f"Using handler {handler} for client {client_socket}")

            if handler.__class__.__name__ == "UserHandler":
                return handler.handle(client_socket) # return state for user handler

            handler.handle(client_socket)

            if client_socket.fileno() == -1:
                logger.info(f"Socket for {client_socket} was closed, ending session.")
                break

            try:
                msg = Message.read(client_socket)
            except StopIteration:
                logger.info("Socket closed, ending session.")
                break

            if str(msg).strip().upper() == "RESET_SESSION":
                logger.info("Client requested reset. Restarting session.")
                continue
            break
