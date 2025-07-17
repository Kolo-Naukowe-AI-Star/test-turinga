from .base import Correspondent


class User(Correspondent):
    """User class that stores messages, until they are processed."""

    def __init__(self, name: str):
        """Initialize a User instance.

        Args:
            name (str): The name of the user.
        """
        self.name = name
        self.queue = []

    def send_message(self, message: str) -> None:
        """Send a message to the user.

        Args:
            message (str): The message to send.
        """
        self.queue.append(message)
        return None

    def pop(self) -> str | None:
        """Pop the next message from the queue.

        Returns:
            str | None: The next message in the queue, or None if the queue is empty.
        """
        return None if not self.queue else self.queue.pop(0)
