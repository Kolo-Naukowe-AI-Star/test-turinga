import socket
import threading

from test_turinga import Message


def receive_messages(client_socket: socket.socket) -> None:
    while True:
        try:
            message = Message.read(client_socket)
            print("Received from partner: " + message)
        except:
            break


def client_program(host: str | None = None, port: int = 5000):
    if host is None:
        host = socket.gethostname()

    client_socket = socket.socket()
    client_socket.connect((host, port))

    # Start a thread to receive messages
    threading.Thread(
        target=receive_messages, args=(client_socket,), daemon=True
    ).start()

    while True:
        client_socket.send(Message(input()).bytes)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser("Turing Test Socket Client")
    parser.add_argument(
        "--host",
        type=str,
        default=None,
        help="Hostname or IP address of the server",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=5000,
        help="Port number of the server",
    )
    args = parser.parse_args()

    client_program(args.host, args.port)
