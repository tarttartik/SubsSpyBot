from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Subscriber:
    user_id: str
    username: Optional[str]
    is_deleted: bool = False
    first_message_date: Optional[datetime] = None