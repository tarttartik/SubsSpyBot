import time
import os
from dotenv import load_dotenv

from utils.logging import setup_logging
from bot.telegram_api import TelegramAPI
from bot.core.handlers import BotHandlers
from bot.core.dialog_manager import DialogManager

def main():
    setup_logging()
    load_dotenv()

    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN not set")

    api = TelegramAPI(token)
    dialog = DialogManager()
    handlers = BotHandlers(api, dialog)

    offset = 0
    print("🤖 Bot started")

    while True:
        updates = api.get_updates(offset)

        for update in updates:
            offset = update["update_id"] + 1
            handlers.handle(update)

        time.sleep(1)

if __name__ == "__main__":
    main()