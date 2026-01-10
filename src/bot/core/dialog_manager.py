from enum import Enum


class UserState(Enum):
    IDLE = "idle"
    AWAITING_FILES = "awaiting_files"
    PROCESSING = "processing"


class DialogManager:
    """Manages user states (FSM)."""

    def __init__(self):
        self._states = {}

    def get_state(self, chat_id):
        return self._states.get(chat_id, UserState.IDLE)

    def set_state(self, chat_id, state: UserState):
        self._states[chat_id] = state