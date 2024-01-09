from typing import Any, List

from ..base import BaseEntity


class ReleaseTypeEntity(BaseEntity):
    def __init__(self, release_id: str, label_en: str, label_jp: str):
        self._release_id = release_id
        self._label_en = label_en
        self._label_jp = label_jp

    @property
    def release_id(self) -> str:
        return self._release_id

    @property
    def label_en(self) -> str:
        return self._label_en

    @property
    def label_jp(self) -> str:
        return self._label_jp

    def check_is_same(self, other: Any) -> bool:
        if not isinstance(other, ReleaseTypeEntity):
            return False
        return self.release_id == other.release_id

    @staticmethod
    def get_columns() -> List[str]:
        return ["release_id", "label_en", "label_jp"]
