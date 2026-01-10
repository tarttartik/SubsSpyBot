from abc import ABC, abstractmethod
from typing import List
from models.subscriber import Subscriber


class FileGeneratorContract(ABC):
    """Interface for generating output from subscribers."""

    @abstractmethod
    def generate(self, subscribers: List[Subscriber]):
        pass