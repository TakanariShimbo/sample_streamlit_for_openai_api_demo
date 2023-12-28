from typing import Any, List

from ..base import BaseEntity


class ChatMessageEntity(BaseEntity):
    def __init__(self, room_id: str, role: str, account_id: str, content: str) -> None:
        self._room_id = room_id
        self._role = role
        self._account_id = account_id
        self._content = content

    @property
    def room_id(self) -> str:
        return self._room_id

    @property
    def role(self) -> str:
        return self._role

    @property
    def account_id(self) -> str:
        return self._account_id

    @property
    def content(self) -> str:
        return self._content

    def check_is_same(self, other: Any) -> bool:
        return False

    @staticmethod
    def get_column_names() -> List[str]:
        return ["room_id", "role", "account_id", "content"]
