from typing import Any, List

from ..base import BaseEntity


class AssistantTypeEntity(BaseEntity):
    def __init__(self, assistant_id: str, label_en: str, label_jp: str):
        self._assistant_id = assistant_id
        self._label_en = label_en
        self._label_jp = label_jp

    @property
    def assistant_id(self) -> str:
        return self._assistant_id

    @property
    def label_en(self) -> str:
        return self._label_en

    @property
    def label_jp(self) -> str:
        return self._label_jp

    def check_is_same(self, other: Any) -> bool:
        if not isinstance(other, AssistantTypeEntity):
            return False
        return self.assistant_id == other.assistant_id

    @staticmethod
    def get_column_names() -> List[str]:
        return ["assistant_id", "label_en", "label_jp"]
