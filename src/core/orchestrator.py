from parsers.telegram_json_parser import TelegramJsonParser
from generators.text_generator import TextGenerator
from generators.excel_generator import ExcelGenerator


class Orchestrator:
    """Coordinates parsing and result generation."""

    def __init__(self):
        self.parser = TelegramJsonParser()
        self.text_generator = TextGenerator()
        self.excel_generator = ExcelGenerator()

    def process(self, files_bytes: list[bytes]):
        subscribers = []

        for file_bytes in files_bytes:
            subscribers.extend(self.parser.parse(file_bytes))

        if not subscribers:
            return {"error": "Участники не найдены."}

        if len(subscribers) <= 50:
            return {
                "type": "text",
                "data": self.text_generator.generate(subscribers),
            }

        excel_bytes, filename = self.excel_generator.generate(subscribers)
        return {
            "type": "excel",
            "filename": filename,
            "bytes": excel_bytes,
        }