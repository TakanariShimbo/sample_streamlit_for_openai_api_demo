from typing import Any, List, Optional

from ..base import BaseEntity


class ChatMessageEntity(BaseEntity):
    def __init__(self, room_id: str, sender_id: str, role: str, content: str, sent_at: Optional[str] = None) -> None:
        self._room_id = room_id
        self._sender_id = sender_id
        self._role = role
        self._content = content
        self._sent_at = sent_at

    @property
    def room_id(self) -> str:
        return self._room_id

    @property
    def sender_id(self) -> str:
        return self._sender_id

    @property
    def role(self) -> str:
        return self._role

    @property
    def content(self) -> str:
        return self._content

    @property
    def sent_at(self) -> Optional[str]:
        sent_at = self._sent_at
        if sent_at == None:
            return sent_at
        return sent_at.split(sep=" ")[0]

    def check_is_same(self, other: Any) -> bool:
        return False

    @staticmethod
    def get_column_names() -> List[str]:
        return ["room_id", "sender_id", "role", "content", "sent_at"]
