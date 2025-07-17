from .correspondents import Correspondent


class Thread:
    """Represents a conversation between multiple abstract correspondents."""

    def __init__(self, *correspondents: Correspondent):
        """Initialize a new thread with the given correspondents.

        Args:
            *correspondents: The correspondents involved in the thread.
        """
        self.correspondents = [*correspondents]
        self.messages: list[tuple[Correspondent, str]] = []

    def received_message(self, sender: Correspondent, message: str) -> None:
        """Handle a message received by the thread.

        Args:
            sender: The sender of the message.
            message: The content of the message.
        """
        self.messages.append((sender, message))
        for correspondent in self.correspondents:
            if correspondent != sender:
                correspondent.send_message(message)

    def __contains__(self, corr: Correspondent) -> bool:
        return corr in self.correspondents
