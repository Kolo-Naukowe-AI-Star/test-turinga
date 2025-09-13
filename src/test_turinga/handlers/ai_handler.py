import logging
from random import choice
from socket import socket

from test_turinga.ai import AgentFactory
from test_turinga.handlers.base import MessageHandler
from test_turinga.message import Message

logger = logging.getLogger(__name__)

MAX_TURNS = 5
TURN_DELAY = 20 # seconds to ensure equal turn time for humans and AI
# turn delay not implemented yet for easier testing


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
        turn_count = 0

        # Send turn notification
        try:
            client_socket.send(Message("TURN:YOU").bytes)
        except Exception:
            pass

        try:
            while True:
                user_message = Message.read(client_socket)

                message_log.append(f"Użytkownik: {user_message}")

                turn_count += 1
                if turn_count >= MAX_TURNS:
                    try:
                        client_socket.send(
                            Message("DECISION: Who do you think it was? HUMAN or AI?").bytes
                        )
                    except Exception:
                        pass

                    try:
                        guess = Message.read(client_socket)
                        guess_text = str(guess).strip().upper()
                        result = "Correct!" if guess_text == "AI" else "Wrong!"
                        client_socket.send(Message(result).bytes)
                    except Exception:
                        pass
                    break

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
