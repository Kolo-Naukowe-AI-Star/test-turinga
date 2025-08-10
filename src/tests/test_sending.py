import unittest
import threading
from socket import socketpair

from test_turinga import Server, Message, AIHandler, UserHandler

from .test_llama import MODEL_PATH


class TestAIHandler(unittest.TestCase):
    def setUp(self):
        self.server = Server([AIHandler(MODEL_PATH)])

    def test_connect_ai(self):
        client_socket, recv_socket = socketpair()
        client_socket.sendall(Message("What's your name?").bytes)
        threading.Thread(target=self.server.handle, args=(recv_socket,)).start()
        resp = Message.read(client_socket)
        self.assertIn("Alex", resp)
        client_socket.close()


class TestUserHandler(unittest.TestCase):
    def setUp(self):
        self.server = Server([UserHandler()])

    def test_connect_us(self):
        a_send, a_recv = socketpair()
        b_send, b_recv = socketpair()
        self.server.handle(a_recv)
        self.server.handle(b_send)
        test_string = Message("Hello, world!")
        a_send.sendall(test_string.bytes)
        resp = Message.read(b_recv)
        self.assertEqual(test_string, resp)
        a_send.close()
        b_recv.close()
