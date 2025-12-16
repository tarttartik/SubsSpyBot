"""Data models used across the application."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Subscriber:
    """Represents a subscriber record parsed from the input source."""

    user_id: Optional[str]
    username: Optional[str]
    name: Optional[str]
    is_deleted: bool = False
