from typing import Any, List

from ..base import BaseEntity


class ChatRoomEntity(BaseEntity):
    def __init__(self, room_id: str, title: str) -> None:
        self._room_id = room_id
        self._title = title

    @property
    def room_id(self) -> str:
        return self._room_id

    @property
    def title(self) -> str:
        return self._title

    def check_is_same(self, other: Any) -> bool:
        return False

    @staticmethod
    def get_column_names() -> List[str]:
        return ["room_id", "title"]
