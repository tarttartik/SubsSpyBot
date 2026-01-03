from typing import List
from models.subscriber import Subscriber


class TextGenerator:
    """Generates plain text output."""

    def generate(self, subscribers: List[Subscriber]) -> str:
        return "\n".join(
            f"{s.username} (id: {s.user_id})" if s.username else s.user_id
            for s in subscribers
        )