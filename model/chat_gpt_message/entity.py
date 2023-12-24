from typing import Any, List

from .. import BaseEntity


class ChatGptMessageEntity(BaseEntity):
    def __init__(self, room_id: str, role: str, sender_id: str, content: str) -> None:
        self._room_id = room_id
        self._role = role
        self._sender_id = sender_id
        self._content = content

    @property
    def room_id(self) -> str:
        return self._room_id

    @property
    def role(self) -> str:
        return self._role

    @property
    def sender_id(self) -> str:
        return self._sender_id

    @property
    def content(self) -> str:
        return self._content

    def check_is_same(self, other: Any) -> bool:
        return False

    @staticmethod
    def get_column_names() -> List[str]:
        return ["room_id", "role", "sender_id", "content"]
