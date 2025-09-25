import logging
import threading
from socket import socket

from .base import MessageHandler
from ..message import Message

logger = logging.getLogger(__name__)


class UserHandler(MessageHandler):
    def __init__(self):
        super().__init__()
        self.waiting_clients: list[socket] = []
        self.lock = threading.Lock()

    def handle(self, client_socket: socket) -> None:
        with self.lock:
            if self.waiting_clients:
                partner_socket = self.waiting_clients.pop(0)
                logger.info(
                    f"Matching human client {client_socket} with {partner_socket}"
                )
                threading.Thread(
                    target=self.handle_turns,
                    args=(client_socket, partner_socket),
                    daemon=True,
                ).start()
            else:
                logger.debug(f"Waiting for human client {client_socket}")
                self.waiting_clients.append(client_socket)

    def handle_turns(self, client_a: socket, client_b: socket):
        current_sender, current_receiver = client_a, client_b
        turn_count = 0

        # Send initial turn notifications
        try:
            current_sender.send(Message("TURN:YOU").bytes)
            current_receiver.send(Message("TURN:WAIT").bytes)
            self.save_time()
        except Exception:
            pass

        try:
            while True:
                message = Message.read(current_sender)
                self.wait()
                current_receiver.send(message.bytes)
                turn_count += 1

                if turn_count >= self.MAX_MESSAGES:
                    self.safe_send(
                        client_a,
                        "DECISION: Who do you think it was? HUMAN or AI?",
                    )
                    self.safe_send(
                        client_b,
                        "DECISION: Who do you think it was? HUMAN or AI?",
                    )
                    try:
                        guess_a = Message.read(client_a)
                        guess_b = Message.read(client_b)
                        result_a = (
                            "Correct!"
                            if str(guess_a).strip().upper() == "HUMAN"
                            else "Wrong!"
                        )
                        result_b = (
                            "Correct!"
                            if str(guess_b).strip().upper() == "HUMAN"
                            else "Wrong!"
                        )
                        self.safe_send(client_a, result_a)
                        self.safe_send(client_b, result_b)
                    except Exception:
                        pass
                    break

                # Swap turns
                current_sender, current_receiver = (
                    current_receiver,
                    current_sender,
                )
                try:
                    self.safe_send(current_sender, "TURN:YOU")
                    self.safe_send(current_receiver, "TURN:WAIT")
                    self.save_time()
                except Exception:
                    pass

        except StopIteration:
            pass
