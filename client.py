import socket
import threading


def receive_messages(client_socket: socket.socket) -> None:
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            print("\nReceived from partner: " + data)
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
        message = input()
        client_socket.send(message.encode())


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
