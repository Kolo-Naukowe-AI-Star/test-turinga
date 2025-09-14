import logging
from abc import ABC, abstractmethod
from socket import socket

from test_turinga.message import Message

logger = logging.getLogger(__name__)


class MessageHandler(ABC):
    """Base class for turn-based conversation handlers."""

    MAX_TURNS = 5

    def __init__(self):
        self.turn_count = 0

    @abstractmethod
    def handle(self, client_socket: socket) -> None: ...

    def safe_send(self, client_socket: socket, msg: str):
        try:
            client_socket.send(Message(msg).bytes)
        except Exception:
            logger.warning(f"Failed to send message: {msg}")

    def increment_turn(self):
        self.turn_count += 1
        return self.turn_count

    def is_max_turns(self):
        return self.turn_count >= self.MAX_TURNS
