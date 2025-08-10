from socket import socket, AF_INET, SOCK_STREAM
import threading
from random import random, choice
import logging

from .ai import AgentFactory

logger = logging.getLogger(__name__)

RECV_BUFFER_SIZE = 1024
AI_CHANCE = 0.5


class Server:
    def __init__(
        self, model_path: str, identity_bank: list[tuple[str, int]] = [("Alex", 25)]
    ):
        self.waiting_clients: list[socket] = []
        self.lock = threading.Lock()
        self.agent_factory = AgentFactory(model_path=model_path)
        self.identity_bank = identity_bank
        logger.info("Server initialized")

    def main(self, host: str, port: int) -> None:
        main_socket = socket(AF_INET, SOCK_STREAM)
        main_socket.bind((host, port))
        main_socket.listen()
        logger.debug(f"Server started on {host}:{port}")

        while True:
            client_socket, addr = main_socket.accept()
            logger.info(f"Accepted connection from {addr}")
            threading.Thread(target=self.client_thread, args=(client_socket,)).start()

    def handle_ai(self, client_socket: socket) -> None:
        logger.debug(f"Attaching AI agent to {client_socket}")
        agent = self.agent_factory.new_agent(*choice(self.identity_bank))
        try:
            while True:
                data = client_socket.recv(RECV_BUFFER_SIZE)
                if not data:
                    break
                user_message = data.decode()
                ai_response = agent.send_message(user_message)
                client_socket.send(ai_response.encode())
        except:
            pass
        finally:
            logger.info(f"Detaching AI agent from {client_socket}")
            client_socket.close()

    def handle_human(self, client_socket: socket) -> None:
        with self.lock:
            if self.waiting_clients:
                partner_socket = self.waiting_clients.pop(0)
                logger.info(
                    f"Matching human client {client_socket} with {partner_socket}"
                )
                # Start relaying messages between the two clients
                threading.Thread(
                    target=handle_client, args=(client_socket, partner_socket)
                ).start()
                threading.Thread(
                    target=handle_client, args=(partner_socket, client_socket)
                ).start()
            else:
                logger.debug(f"Waiting for human client {client_socket}")
                self.waiting_clients.append(client_socket)

    def client_thread(self, client_socket: socket) -> None:
        if (
            random() > AI_CHANCE
        ):  # True - match with AI, False - wait for human TODO: add better matchmaking
            self.handle_ai(client_socket)
        else:
            self.handle_human(client_socket)


def handle_client(client_socket: socket, partner_socket: socket) -> None:
    try:
        while True:
            data = client_socket.recv(RECV_BUFFER_SIZE)
            if not data:
                break
            partner_socket.send(data)
    except:
        pass
    finally:
        client_socket.close()
        partner_socket.close()
