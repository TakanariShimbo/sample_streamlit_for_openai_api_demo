from typing import Any, List, Optional

from ..base import BaseEntity


class ChatRoomEntity(BaseEntity):
    def __init__(self, room_id: str, account_id: str, title: str, created_at: Optional[str] = None) -> None:
        self._room_id = room_id
        self._account_id = account_id
        self._title = title
        self._created_at = created_at

    @property
    def room_id(self) -> str:
        return self._room_id

    @property
    def account_id(self) -> str:
        return self._account_id

    @property
    def title(self) -> str:
        return self._title

    @property
    def created_at(self) -> Optional[str]:
        created_at = self._created_at
        if created_at == None:
            return created_at
        return created_at.split(sep=" ")[0]

    def check_is_same(self, other: Any) -> bool:
        return False

    @staticmethod
    def get_column_names() -> List[str]:
        return ["room_id", "account_id", "title", "created_at"]
