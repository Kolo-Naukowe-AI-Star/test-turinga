import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            print('\nReceived from partner: ' + data)
        except:
            break

def client_program():
    host = socket.gethostname()
    port = 5000  # Make sure this matches your server

    client_socket = socket.socket()
    client_socket.connect((host, port))

    # Start a thread to receive messages
    threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()

    while True:
        message = input()
        if message.lower().strip() == 'bye':
            client_socket.close()
            break
        client_socket.send(message.encode())

if __name__ == '__main__':
    client_program()