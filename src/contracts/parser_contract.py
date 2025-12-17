"""Interface for parsing subscriber data from files."""

from abc import ABC, abstractmethod
from typing import List

from ..models.subscriber import Subscriber


class ParserContract(ABC):
    """Contract that defines how parsers should convert files to subscribers."""

    @abstractmethod
    def parse(self, file_path: str) -> List[Subscriber]:
        """Read the file at ``file_path`` and return a list of subscribers."""
        raise NotImplementedError
