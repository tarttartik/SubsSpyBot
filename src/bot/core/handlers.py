import logging
import threading

from bot.core.messages import BotMessages
from bot.core.dialog_manager import UserState
from core.orchestrator import Orchestrator


class BotHandlers:
    """Core bot logic (commands & files)."""

    def __init__(self, api, dialog_manager):
        self.api = api
        self.dialog = dialog_manager
        self.orchestrator = Orchestrator()
        self.files = {}

    def handle(self, update: dict):
        """
        Entry point for all incoming Telegram updates.
        """
        message = update.get("message")
        if not message:
            return

        chat_id = message.get("chat", {}).get("id")
        if not chat_id:
            return

        text = message.get("text", "")
        document = message.get("document")

        logging.info(f"Incoming update from chat {chat_id}")

        if text.startswith("/start"):
            self.handle_start(chat_id)

        elif text.startswith("/help"):
            self.handle_help(chat_id)

        elif document:
            file_id = document.get("file_id")
            if not file_id:
                return

            file_bytes = self.api.download_file(file_id)
            self.handle_file(chat_id, file_bytes)

        else:
            self.api.send_message(chat_id, BotMessages.UNKNOWN_COMMAND)

    def handle_start(self, chat_id):
        self.dialog.set_state(chat_id, UserState.AWAITING_FILES)
        self.files[chat_id] = []
        self.api.send_message(chat_id, BotMessages.START)

    def handle_help(self, chat_id):
        self.api.send_message(chat_id, BotMessages.HELP)

    def handle(self, update: dict):
        message = update.get("message")
        if not message:
            return

        chat_id = message.get("chat", {}).get("id")
        if not chat_id:
            return

        text = message.get("text", "")
        documents = []

        if message.get("document"):
            documents.append(message["document"])

        if message.get("media_group_id") and message.get("media"):
            for media_item in message["media"]:
                if media_item.get("document"):
                    documents.append(media_item["document"])

        logging.info(f"Incoming update from chat {chat_id}")

        if text.startswith("/start"):
            self.handle_start(chat_id)

        elif text.startswith("/help"):
            self.handle_help(chat_id)

        elif documents:
            if len(documents) > 10:
                self.api.send_message(chat_id, "❌ Можно отправить максимум 10 файлов за раз.")
                documents = documents[:10]

            self.dialog.set_state(chat_id, UserState.PROCESSING)

            threading.Thread(
                target=self._process_multiple_files,
                args=(chat_id, documents),
                daemon=True
            ).start()

        else:
            self.api.send_message(chat_id, BotMessages.UNKNOWN_COMMAND)

    def _process_multiple_files(self, chat_id, documents):
        try:
            for idx, doc in enumerate(documents, start=1):
                file_id = doc.get("file_id")
                if not file_id:
                    continue

                file_bytes = self.api.download_file(file_id)
                result = self.orchestrator.process([file_bytes])  # обрабатываем один файл за раз

                if "error" in result:
                    self.api.send_message(chat_id, f"Ошибка при обработке файла {idx}: {result['error']}")
                elif result["type"] == "text":
                    self.api.send_message(chat_id, f"Результат:\n{result['data']}")
                else:
                    self.api.send_document(
                        chat_id,
                        result['filename'],
                        result["bytes"]
                   )
        except Exception:
            logging.exception("Processing failed")
            self.api.send_message(chat_id, BotMessages.UNKNOWN_ERROR)
        finally:
            self.dialog.set_state(chat_id, UserState.IDLE)