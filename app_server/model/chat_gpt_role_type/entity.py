from typing import Any, List

from ..base import BaseEntity


class ChatGptRoleTypeEntity(BaseEntity):
    def __init__(self, role_id: str, label_en: str, label_jp: str):
        self._role_id = role_id
        self._label_en = label_en
        self._label_jp = label_jp

    @property
    def role_id(self) -> str:
        return self._role_id

    @property
    def label_en(self) -> str:
        return self._label_en

    @property
    def label_jp(self) -> str:
        return self._label_jp

    def check_is_same(self, other: Any) -> bool:
        if not isinstance(other, ChatGptRoleTypeEntity):
            return False
        return self.role_id == other.role_id

    @staticmethod
    def get_column_names() -> List[str]:
        return ["role_id", "label_en", "label_jp"]
