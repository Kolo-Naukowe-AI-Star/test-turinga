import unittest

from test_turinga import Message


class MessageTest(unittest.TestCase):
    def test_message_creation(self):
        message = Message("Hello")
        self.assertEqual(message.bytes, b"\x05\x00\x00\x00Hello")

    def test_invalid_message(self):
        with self.assertRaises(ValueError):
            Message(" " * int(1e10))
