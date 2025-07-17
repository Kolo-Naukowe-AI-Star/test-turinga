from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Correspondent(ABC):
    """Abstract base class for correspondents."""

    name: str

    @abstractmethod
    def send_message(self, message: str) -> str | None: ...
