import pytest

from test_turinga.message import Message


def test_message_creation():
    message = Message("Hello")
    assert message.bytes == b"\x05\x00\x00\x00Hello"


def test_invalid_message():
    with pytest.raises(ValueError):
        Message(" " * int(1e10))
