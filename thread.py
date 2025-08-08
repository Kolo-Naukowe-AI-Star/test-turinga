import threading

def handle_client(client_socket):
    # This function is responsible for handling each client connection.
    # It sends a greeting message to the client and then closes the connection.
    client_socket.send(b"Hello, Client!")
    client_socket.close()

while True:
    # The server continuously listens for incoming client connections.
    client_socket, addr = server_socket.accept()
    # When a new client connects, a new thread is created to handle the client.
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()