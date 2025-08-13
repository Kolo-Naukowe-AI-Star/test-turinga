from struct import pack, unpack, error as StructError
from socket import socket

MAX_LEN = 2**32 - 1


# Our implementation of a binary serializer for messages
# It sort of works like a pascal string, but with 4 bytes of length instead of one
# Ideally, something like elias gamma encoding for length would've been better, but hey it works, and I'm not doing bit manipulation in Python


class Message(str):
    def __new__(cls, content: str):
        if len(content) > MAX_LEN:
            raise ValueError(f"Content too long: {len(content)} > {MAX_LEN}")
        return super().__new__(cls, content)

    @property
    def bytes(self) -> bytes:
        b = self.encode()
        return pack("I", len(b)) + b

    @staticmethod
    def read(sock: socket) -> "Message":
        try:
            length = unpack("I", sock.recv(4))[0]
        except StructError:
            raise StopIteration("Invalid message length")
        content = sock.recv(length).decode()
        return Message(content)
