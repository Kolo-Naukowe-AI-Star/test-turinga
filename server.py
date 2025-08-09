from src.ai import AgentFactory

import socket
import threading
import argparse
from random import choice

waiting_clients = []
lock = threading.Lock()

def handle_ai(client_socket):
    agent = agent_factory.new_agent(name="Alex", age=25) # for now its always alex, 25 -- TODO: make it dynamic (randomize?)
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            user_message = data.decode()
            ai_response = agent.send_message(user_message)
            client_socket.send(ai_response.encode())
    except:
        pass
    finally:
        client_socket.close()

def handle_client(client_socket, partner_socket):
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            partner_socket.send(data)
    except:
        pass
    finally:
        client_socket.close()
        partner_socket.close()

def client_thread(client_socket):
    global waiting_clients

    if choice([True, False]): # True - match with AI, False - wait for human TODO: add better matchmaking
        threading.Thread(target=handle_ai, args=(client_socket,), daemon=True).start()
    else:
        with lock:
            if waiting_clients:
                partner_socket = waiting_clients.pop(0)
                # Start relaying messages between the two clients
                threading.Thread(target=handle_client, args=(client_socket, partner_socket)).start()
                threading.Thread(target=handle_client, args=(partner_socket, client_socket)).start()
            else:
                waiting_clients.append(client_socket)

def run_socket_server(model_path, host, port):
    global agent_factory, HOST, PORT
    agent_factory = AgentFactory(model_path=model_path)
    HOST = host
    PORT = port
    main()

def main():
    server_socket = socket.socket()
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print("Server listening...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        threading.Thread(target=client_thread, args=(client_socket,)).start()

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Turing Test Socket Server")
    parser.add_argument("--model_path", type=str, default="./llama-2-13b-chat.Q5_K_M.gguf", help="Path to the LLM model")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to listen on")
    parser.add_argument("--port", type=int, default=5000, help="Port to listen on")
    args = parser.parse_args()

    run_socket_server(args.model_path, args.host, args.port)