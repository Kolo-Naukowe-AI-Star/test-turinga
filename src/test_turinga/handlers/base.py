from abc import ABC, abstractmethod
from socket import socket


class MessageHandler(ABC):

    @abstractmethod
    def handle(self, client_socket: socket) -> None: ...
