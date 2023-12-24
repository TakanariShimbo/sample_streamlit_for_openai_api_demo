from typing import Any, List

from .. import BaseEntity


class PageTypeEntity(BaseEntity):
    def __init__(self, key: str, label_en: str, label_jp: str):
        self._key = key
        self._label_en = label_en
        self._label_jp = label_jp

    @property
    def key(self) -> str:
        return self._key

    @property
    def label_en(self) -> str:
        return self._label_en

    @property
    def label_jp(self) -> str:
        return self._label_jp

    def check_is_same(self, other: Any) -> bool:
        if not isinstance(other, PageTypeEntity):
            return False
        return self.key == other.key

    @staticmethod
    def get_column_names() -> List[str]:
        return ["key", "label_en", "label_jp"]
