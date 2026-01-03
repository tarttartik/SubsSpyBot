import requests
import logging
from typing import List, Dict, Any


class TelegramAPI:
    def __init__(self, token: str):
        self.token = token
        self.base_url = f"https://api.telegram.org/bot{token}"

    def get_updates(self, offset: int = 0, timeout: int = 10) -> List[Dict[str, Any]]:
        """
        Poll updates from Telegram API.
        """
        try:
            response = requests.get(
                f"{self.base_url}/getUpdates",
                params={
                    "offset": offset,
                    "timeout": timeout,
                },
                timeout=timeout + 5,
            )
            data = response.json()

            if not data.get("ok"):
                logging.error(f"Telegram API error: {data}")
                return []

            return data.get("result", [])

        except Exception as e:
            logging.exception(f"Failed to get updates: {e}")
            return []

    def send_message(self, chat_id: int, text: str):
        """
        Send text message to user.
        """
        try:
            requests.post(
                f"{self.base_url}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": text,
                },
                timeout=5,
            )
        except Exception as e:
            logging.exception(f"Failed to send message: {e}")

    def send_document(self, chat_id: int, filename: str, file_bytes: bytes):
        """
        Send document (Excel file).
        """
        try:
            files = {
                "document": (filename, file_bytes)
            }
            data = {
                "chat_id": chat_id,
            }

            requests.post(
                f"{self.base_url}/sendDocument",
                data=data,
                files=files,
                timeout=30,
            )
        except Exception as e:
            logging.exception(f"Failed to send document: {e}")

    def download_file(self, file_id: str) -> bytes:
        """
        Get file from Telegram and return it as bytes.
        Processing ONLY in memory.
        """
        try:
            # 1️⃣ Получаем информацию о файле (путь на сервере Telegram)
            resp = requests.get(f"{self.base_url}/getFile", params={"file_id": file_id}, timeout=10)
            resp.raise_for_status()
            data = resp.json()

            if not data.get("ok"):
                logging.error(f"Failed to get file info: {data}")
                return b""

            file_path = data["result"]["file_path"]

            # 2️⃣ Скачиваем файл в память
            file_url = f"https://api.telegram.org/file/bot{self.token}/{file_path}"
            file_resp = requests.get(file_url, timeout=30)
            file_resp.raise_for_status()

            return file_resp.content  # возвращаем байты файла

        except Exception as e:
            logging.exception(f"Failed to download file: {e}")
            return b""