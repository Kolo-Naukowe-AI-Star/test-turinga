import logging
import time
from abc import ABC, abstractmethod
from socket import socket

from ..message import Message

logger = logging.getLogger(__name__)


class MessageHandler(ABC):
    """Base class for turn-based conversation handlers."""

    MAX_MESSAGES = 10
    MIN_TURN_DURATION = 8

    def __init__(self):
        self.turn_count = 0
        self.turn_time = 0

    @abstractmethod
    def handle(self, client_socket: socket) -> None: ...

    def safe_send(self, client_socket: socket, message: str):
        try:
            client_socket.send(Message(message).bytes)
        except Exception:
            logger.warning(f"Failed to send message: {message}")

    def increment_turn(self):
        self.turn_count += 1
        return self.turn_count

    def is_max_turns(self):
        """Return True if 10 messages have been sent (5 full turns)"""
        return self.turn_count >= self.MAX_MESSAGES

    def save_time(self):
        self.turn_time = time.monotonic()

    def wait(self):
        elapsed = time.monotonic() - self.turn_time
        waiting_time = max(self.MIN_TURN_DURATION - elapsed, 0)
        print(f"waiting {waiting_time:.2f} seconds")
        time.sleep(waiting_time)
