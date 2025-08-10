from socket import socket
import logging
from random import choice

from .base import MessageHandler
from ..message import Message
from ..ai import AgentFactory

logger = logging.getLogger(__name__)


class AIHandler(MessageHandler):
    def __init__(
        self, model_path: str, identity_bank: list[tuple[str, int]] = [("Alex", 25)]
    ):
        super().__init__()
        self.agent_factory = AgentFactory(model_path)
        self.identity_bank = identity_bank

    def handle(self, client_socket: socket) -> None:
        logger.debug(f"Attaching AI agent to {client_socket}")
        message_log: list[Message] = []
        agent = self.agent_factory.new_agent(*choice(self.identity_bank))
        try:
            while True:
                user_message = Message.read(client_socket)
                client_socket.send(
                    Message(agent.send_message(user_message, message_log)).bytes
                )
                message_log.append(user_message)
        except StopIteration:
            pass
        finally:
            logger.info(f"Detaching AI agent from {client_socket}")
            client_socket.close()
