import threading
from socket import socket
import logging

from .base import MessageHandler
from ..message import Message

logger = logging.getLogger(__name__)


class UserHandler(MessageHandler):
    def __init__(self):
        self.waiting_clients: list[socket] = []
        self.lock = threading.Lock()
        super().__init__()

    def handle(self, client_socket: socket) -> None:
        with self.lock:
            if self.waiting_clients:
                partner_socket = self.waiting_clients.pop(0)
                logger.info(
                    f"Matching human client {client_socket} with {partner_socket}"
                )
                # Start relaying messages between the two clients
                threading.Thread(
                    target=handle_client, args=(client_socket, partner_socket)
                ).start()
                threading.Thread(
                    target=handle_client, args=(partner_socket, client_socket)
                ).start()
            else:
                logger.debug(f"Waiting for human client {client_socket}")
                self.waiting_clients.append(client_socket)


def handle_client(client_socket: socket, partner_socket: socket) -> None:
    try:
        while True:
            partner_socket.send(Message.read(client_socket).bytes)
    except StopIteration:
        pass
    finally:
        client_socket.close()
        partner_socket.close()
