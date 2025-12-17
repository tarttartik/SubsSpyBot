import json
import os
from typing import List, Dict, Any
from datetime import datetime
import re  
import logging

from ..contracts.parser_contract import ParserContract
from ..models.subscriber import Subscriber

class TelegramParser(ParserContract):
    """Parses a Telegram export JSON file and extracts subscriber information."""
    def parse(self, file_path: str) -> List[Subscriber]:
        """Args:
            file_path (str): Path to the JSON file.
        
        Returns:
            List[Subscriber]: List of Subscriber objects.
        
        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the JSON is invalid or parsing fails.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        try:
            """Load JSON data from file"""
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in file {file_path}: {e}")
        
        subscribers: Dict[str, Subscriber] = {}
        messages = data.get("messages", [])
        
        for message in messages:
            if not isinstance(message, dict):
                continue
            
            """Extract sender info"""
            from_field = message.get("from")
            from_id = message.get("from_id")
            
            if not from_id:
                """Fallback: generate a unique ID based on username or name"""
                username = from_field or ""
                name = from_field or ""
                fallback_id = f"fallback_{hash(username + name) % 1000000}"
                from_id = fallback_id
                logging.warning(f"No 'from_id' found for user '{from_field}', using fallback ID: {fallback_id}")
            
            user_id = str(from_id)
            username = message.get("from", "")  
            name = message.get("from", "")  
            
            """Parse message date"""
            date_str = message.get("date")
            if date_str:
                try:
                    message_date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                except ValueError:
                    message_date = None
            else:
                message_date = None
            
            """Update or create subscriber"""
            if user_id not in subscribers:
                subscribers[user_id] = Subscriber(
                    user_id=user_id,
                    username=username,
                    name=name,
                    is_deleted=False,
                    first_message_date=message_date
                )
            else:
                """Update first_message_date if this is earlier"""
                existing = subscribers[user_id]
                if message_date and (not existing.first_message_date or message_date < existing.first_message_date):
                    existing.first_message_date = message_date
                        
            text = message.get("text", "")
            if isinstance(text, list):
                for entity in text:
                    if isinstance(entity, dict) and entity.get("type") == "mention":
                        mention_username = entity.get("text", "").lstrip("@")
                        if mention_username:
                            mention_id = f"mention_{mention_username}"
                            if mention_id not in subscribers:
                                subscribers[mention_id] = Subscriber(
                                    user_id=mention_id,
                                    username=mention_username,
                                    name="",  
                                    is_deleted=False,
                                    first_message_date=None  
                                )
            elif isinstance(text, str):
                pass
        
        logging.info(f"Parsed {len(subscribers)} subscribers from {file_path}")
        return list(subscribers.values())
    