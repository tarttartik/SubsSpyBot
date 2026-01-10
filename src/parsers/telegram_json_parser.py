import json
import logging
from datetime import datetime
from typing import Dict, List

from contracts.parser_contract import ParserContract
from models.subscriber import Subscriber


class TelegramJsonParser(ParserContract):
    """Parses Telegram chat export JSON files."""

    def parse(self, file_bytes: bytes) -> List[Subscriber]:
        try:
            data = json.loads(file_bytes.decode("utf-8"))
        except Exception as e:
            raise ValueError(f"Invalid JSON: {e}")

        messages = data.get("messages", [])
        users: Dict[str, Subscriber] = {}

        for msg in messages:
            if not isinstance(msg, dict):
                continue

            user_id = msg.get("from_id")
            username = msg.get("from")
            date_str = msg.get("date")

            if not user_id:
                continue

            # Приведение user_id к строке
            user_id = str(user_id)

            # Парсим дату первого сообщения
            msg_date = None
            if date_str:
                try:
                    msg_date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
                except ValueError:
                    pass

            if user_id not in users:
                users[user_id] = Subscriber(
                    user_id=user_id,
                    username=username,
                    first_message_date=msg_date,
                )
            else:
                existing = users[user_id]
                if msg_date and (not existing.first_message_date or msg_date < existing.first_message_date):
                    existing.first_message_date = msg_date

        logging.info("Parsed %d subscribers", len(users))
        return list(users.values())