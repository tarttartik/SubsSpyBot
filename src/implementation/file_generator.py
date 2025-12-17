import json
import logging
from typing import List
from ..contracts.file_generator_contract import FileGeneratorContract
from ..models.subscriber import Subscriber

class JsonFileGenerator(FileGeneratorContract):
    """ Generates JSON output from a list of Subscriber objects."""
    def generate(self, subscribers: List[Subscriber]) -> str:
        try:
            data = {
                "subscribers": [
                    {
                        "user_id": sub.user_id,
                        "username": sub.username,
                        "name": sub.name,
                        "is_deleted": sub.is_deleted,
                        "first_message_date": sub.first_message_date.isoformat() if sub.first_message_date else None
                    }
                    for sub in subscribers
                ]
            }
            """Serialize to JSON with indentation and UTF-8 support"""
            json_output = json.dumps(data, indent=4, ensure_ascii=False)
            logging.info(f"Generated JSON for {len(subscribers)} subscribers.")
            return json_output
        except Exception as e:
            logging.error(f"Error generating JSON: {e}")
            raise ValueError(f"Failed to generate JSON: {e}")
