import logging
import threading
from socket import socket

from test_turinga.handlers.base import MessageHandler
from test_turinga.message import Message

logger = logging.getLogger(__name__)

MAX_TURNS = 10
TURN_DELAY = 20  # seconds to ensure equal turn time for humans and AI
# turn delay not implemented yet for easier testing


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
                threading.Thread(
                    target=handle_turns, args=(client_socket, partner_socket)
                ).start()
            else:
                logger.debug(f"Waiting for human client {client_socket}")
                self.waiting_clients.append(client_socket)


def handle_turns(client_a: socket, client_b: socket) -> None:
    current_sender = client_a
    current_receiver = client_b
    turn_count = 0

    # Send initial turn notifications to frontends
    try:
        client_a.send(Message("TURN:YOU").bytes)
        client_b.send(Message("TURN:WAIT").bytes)
    except Exception:
        pass

    try:
        while True:
            message = Message.read(current_sender)
            current_receiver.send(message.bytes)
            turn_count += 1

            if turn_count >= MAX_TURNS:
                try:
                    client_a.send(
                        Message(
                            "DECISION: Who do you think it was? HUMAN or AI?"
                        ).bytes
                    )
                    client_b.send(
                        Message(
                            "DECISION: Who do you think it was? HUMAN or AI?"
                        ).bytes
                    )
                except Exception:
                    pass

                try:
                    guess_a = Message.read(client_a)
                    guess_b = Message.read(client_b)

                    guess_a_text = str(guess_a).strip().upper()
                    guess_b_text = str(guess_b).strip().upper()
                    result_a = (
                        "Correct!" if guess_a_text == "HUMAN" else "Wrong!"
                    )
                    result_b = (
                        "Correct!" if guess_b_text == "HUMAN" else "Wrong!"
                    )

                    client_a.send(Message(result_a).bytes)
                    client_b.send(Message(result_b).bytes)
                except Exception:
                    pass
                break

            # Swap turns
            current_sender, current_receiver = current_receiver, current_sender

            # Send notifications to clients
            try:
                current_sender.send(Message("TURN:YOU").bytes)
                current_receiver.send(Message("TURN:WAIT").bytes)
            except Exception:
                pass

    except StopIteration:
        pass
    finally:
        pass
