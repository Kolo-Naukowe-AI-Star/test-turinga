import logging
import random
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
        message_log: list[str] = []
        agent = self.agent_factory.new_agent(*random.choice(self.identity_bank))

        ai_starts = random.choice([True, False])
        starting_player = "ai" if ai_starts else "player"
        logger.debug(f"starting_player: {starting_player}")

        if ai_starts:
            self.safe_send(client_socket, "TURN:WAIT")
            self.save_time()
            logger.debug("AI is starting the conversation...")
            # AI sends first message (history is empty)
            response = agent.send_message(None, message_log)
            logger.debug(f"AI response: {response}")
            message_log.append(f"Partner: {response}")
            self.safe_send(client_socket, response)
            self.wait()
            self.increment_turn()

        try:
            while True:
                self.safe_send(client_socket, "TURN:YOU")
                logger.debug("Waiting for user message...")
                user_message = Message.read(client_socket)
                logger.debug(f"Received from user: {user_message}")
                message_log.append(f"Użytkownik: {user_message}")
                self.increment_turn()

                if self.is_max_turns():
                    break

                self.safe_send(client_socket, "TURN:WAIT")
                logger.debug("AI generating response...")
                response = agent.send_message(str(user_message), message_log)
                logger.debug(f"AI response: {response}")
                message_log.append(f"Partner: {response}")
                self.safe_send(client_socket, response)
                self.increment_turn()

                if self.is_max_turns():
                    break

            # Turn limit reached
            logger.debug("Max turns reached, sending decision prompt")
            self.safe_send(
                client_socket, "DECISION: Who do you think it was? HUMAN or AI?"
            )
            guess = Message.read(client_socket)
            logger.debug(f"User guess: {guess}")
            guess_text = str(guess).strip().upper()
            result = "Correct!" if guess_text == "AI" else "Wrong!"
            self.safe_send(client_socket, result)

        except StopIteration:
            logger.debug("Conversation stopped by StopIteration")
        except Exception as e:
            logger.error(f"Exception in AIHandler: {e}")
        finally:
            logger.info(f"Detaching AI agent from {client_socket}")
