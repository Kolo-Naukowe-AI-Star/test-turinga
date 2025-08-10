import unittest
import threading
from socket import socketpair

from test_turinga import Server

from .test_llama import MODEL_PATH


class TestServer(unittest.TestCase):
    def setUp(self):
        self.server = Server(MODEL_PATH)

    def test_connect_ai(self):
        client_socket, recv_socket = socketpair()
        client_socket.sendall(b"What's your name?")
        threading.Thread(target=self.server.handle_ai, args=(recv_socket,)).start()
        resp = client_socket.recv(1024)
        self.assertIn(b"Alex", resp)
        client_socket.close()

    def test_connect_us(self):
        a_send, a_recv = socketpair()
        b_send, b_recv = socketpair()
        self.server.handle_human(a_recv)
        self.server.handle_human(b_send)
        test_string = b"Hello, world!"
        a_send.sendall(test_string)
        resp = b_recv.recv(1024)
        self.assertEqual(test_string, resp)
        a_send.close()
        b_recv.close()
