import logging
from random import choice
from socket import socket

from test_turinga.ai import AgentFactory
from test_turinga.handlers.base import MessageHandler
from test_turinga.message import Message

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

        # Send turn notification
        try:
            client_socket.send(Message("TURN:YOU").bytes)
        except Exception:
            pass

        try:
            while True:
                user_message = Message.read(client_socket)

                message_log.append(f"Użytkownik: {user_message}")
                response = agent.send_message(user_message, message_log)

                message_log.append(f"Partner: {response}")
                client_socket.send(Message(response).bytes)
                # turn back to user
                try:
                    client_socket.send(Message("TURN:YOU").bytes)
                except Exception:
                    pass

        except StopIteration:
            pass
        finally:
            logger.info(f"Detaching AI agent from {client_socket}")
            client_socket.close()
