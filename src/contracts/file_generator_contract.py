"""Interface for generating output files from subscriber data."""

from abc import ABC, abstractmethod
from typing import List

from models.subscriber import Subscriber


class FileGeneratorContract(ABC):
    """Contract for components that transform subscribers into an output file."""

    @abstractmethod
    def generate(self, subscribers: List[Subscriber]) -> str:
        """Generate a file from ``subscribers`` and return the resulting file path."""
        raise NotImplementedError
