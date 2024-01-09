from typing import Any, List

from ..base import BaseEntity


class ManagementComponentTypeEntity(BaseEntity):
    def __init__(self, component_id: str, label_en: str, label_jp: str):
        self._component_id = component_id
        self._label_en = label_en
        self._label_jp = label_jp

    @property
    def component_id(self) -> str:
        return self._component_id

    @property
    def label_en(self) -> str:
        return self._label_en

    @property
    def label_jp(self) -> str:
        return self._label_jp

    def check_is_same(self, other: Any) -> bool:
        if not isinstance(other, ManagementComponentTypeEntity):
            return False
        return self.component_id == other.component_id

    @staticmethod
    def get_columns() -> List[str]:
        return ["component_id", "label_en", "label_jp"]
