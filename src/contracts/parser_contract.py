from abc import ABC, abstractmethod
from typing import List
from models.subscriber import Subscriber


class ParserContract(ABC):
    """Interface for parsing subscribers from input data."""

    @abstractmethod
    def parse(self, file_bytes: bytes) -> List[Subscriber]:
        pass