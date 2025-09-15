import logging
import time
from abc import ABC, abstractmethod
from socket import socket

from test_turinga.message import Message

logger = logging.getLogger(__name__)


class MessageHandler(ABC):
    """Base class for turn-based conversation handlers."""

    MAX_MESSAGES = 10
    MIN_TURN_DURATION = 20

    def __init__(self):
        self.turn_count = 0
        self.last_turn_time = 0

    @abstractmethod
    def handle(self, client_socket: socket) -> None: ...

    def safe_send(self, client_socket: socket, message: str):
        # Enforce minimum turn time
        if "TURN:" in message:
            self.save_time()
        else:
            self.wait()

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
        self.last_turn_time = time.time()

    def wait(self):
        elapsed = time.time() - self.last_turn_time
        if elapsed < self.MIN_TURN_DURATION:
            time.sleep(self.MIN_TURN_DURATION - elapsed)
