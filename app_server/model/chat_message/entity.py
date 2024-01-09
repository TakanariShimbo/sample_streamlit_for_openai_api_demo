from typing import Any, List, Optional

from ..base import BaseEntity


class ChatMessageEntity(BaseEntity):
    def __init__(self, room_id: str, sender_id: str, role_id: str, content: str, message_serial_id: Optional[int] = None, sent_at: Optional[str] = None) -> None:
        self._message_serial_id = message_serial_id
        self._room_id = room_id
        self._sender_id = sender_id
        self._role_id = role_id
        self._content = content
        self._sent_at = sent_at

    @property
    def message_serial_id(self) -> int:
        message_serial_id = self._message_serial_id
        if message_serial_id == None:
            raise ValueError("Not accessible due to have not constracted.")
        return message_serial_id

    @property
    def room_id(self) -> str:
        return self._room_id

    @property
    def sender_id(self) -> str:
        return self._sender_id

    @property
    def role_id(self) -> str:
        return self._role_id

    @property
    def content(self) -> str:
        return self._content

    @property
    def sent_at(self) -> str:
        sent_at = self._sent_at
        if sent_at == None:
            raise ValueError("Not accessible due to have not constracted.")
        return sent_at.split(sep=" ")[0]

    def check_is_same(self, other: Any) -> bool:
        return False

    @staticmethod
    def get_columns() -> List[str]:
        return ["message_serial_id", "room_id", "sender_id", "role_id", "content", "sent_at"]
