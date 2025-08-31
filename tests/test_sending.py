import threading
from socket import socketpair
from time import sleep

import pytest

from test_turinga.handlers.ai_handler import AIHandler
from test_turinga.handlers.user_handler import UserHandler
from test_turinga.message import Message
from test_turinga.server import Server

from .test_llama import MODEL_PATH


@pytest.fixture
def ai_server():
    server = Server([AIHandler(MODEL_PATH)])
    return server


@pytest.fixture
def user_server():
    server = Server([UserHandler()])
    return server


def read_real_message(sock, timeout=2.0):
    """Read until we get a real message (skip TURN messages)."""
    import time

    start = time.time()
    while True:
        if time.time() - start > timeout:
            return None
        try:
            msg = Message.read(sock)
        except StopIteration:
            return None
        text = str(msg)
        if text.startswith("TURN:"):
            continue
        return msg


def test_connect_ai(ai_server):
    client_socket, recv_socket = socketpair()

    # Start server thread
    thread = threading.Thread(target=ai_server.handle, args=(recv_socket,), daemon=True)
    thread.start()

    sleep(0.05)  # Let server send TURN messages

    client_socket.sendall(Message("What's your name?").bytes)

    resp = read_real_message(client_socket)
    client_socket.close()
    recv_socket.close()
    thread.join(timeout=1)

    assert resp is not None, "Did not receive AI response"
    assert "Alex" in str(resp)


# FIX: this test never passes, possible problem with sockets and TURN messages
def test_connect_user(user_server):
    a_send, a_recv = socketpair()
    b_send, b_recv = socketpair()

    threading.Thread(target=user_server.handle, args=(a_recv,), daemon=True).start()
    threading.Thread(target=user_server.handle, args=(b_send,), daemon=True).start()

    test_string = Message("Hello, world!")
    a_send.sendall(test_string.bytes)

    resp = read_real_message(b_recv)
    a_send.close()
    b_recv.close()
    b_send.close()
    a_recv.close()

    assert resp == test_string
