"""Orchestrator that connects parser and file generator components."""

from typing import List

from ..contracts.file_generator_contract import FileGeneratorContract
from ..contracts.parser_contract import ParserContract
from ..models.subscriber import Subscriber


class Orchestrator:
    """Coordinates parsing input data and producing the resulting output file."""

    def __init__(self, parser: ParserContract, generator: FileGeneratorContract) -> None:
        """Store the parser and file generator implementations."""
        self._parser = parser
        self._generator = generator

    def run(self, file_path: str) -> str:
        """Parse subscribers from ``file_path`` and generate the output file."""
        subscribers: List[Subscriber] = self._parser.parse(file_path)
        return self._generator.generate(subscribers)
