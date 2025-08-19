import socket
import threading

from test_turinga import Message


def receive_messages(client_socket: socket.socket, can_send_event: threading.Event) -> None:
    while True:
        try:
            message = Message.read(client_socket)
            text = str(message)
            
            # Handle turn control messages
            if text.startswith("TURN:"):
                if text == "TURN:YOU":
                    can_send_event.set()
                    print("Your turn.")
                elif text == "TURN:WAIT":
                    can_send_event.clear()
                    print("Please wait for your turn...")
                continue
            
            print("Received from partner: " + text)
        except Exception:
            break


def client_program(host: str | None = None, port: int = 5000):
    if host is None:
        host = socket.gethostname()

    client_socket = socket.socket()
    client_socket.connect((host, port))

    # Turn-based control - start disabled until server grants turn
    can_send_event = threading.Event()

    # Start a thread to receive messages
    threading.Thread(
        target=receive_messages, args=(client_socket, can_send_event), daemon=True
    ).start()

    print("Waiting for your turn...")
    
    while True:
        text = input()
        if not can_send_event.is_set():
            print("Not your turn. Please wait.")
            continue
        client_socket.send(Message(text).bytes)


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
