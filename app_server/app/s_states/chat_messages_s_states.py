from ..base import BaseSState
from controller import ChatMessagesManager


class ChatMessagesSState(BaseSState[ChatMessagesManager]):
    @staticmethod
    def get_name() -> str:
        return "CHAT_MESSAGES_MANAGER"
