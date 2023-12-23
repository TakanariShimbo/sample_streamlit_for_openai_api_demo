from typing import Any, Dict

import pandas as pd

from .. import BaseEntity


class ChatGptModelTypeEntity(BaseEntity):
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

    def to_dict(self) -> Dict[str, Any]:
        return {
            "key": self.key,
            "label_en": self.label_en,
            "label_jp": self.label_jp,
        }

    def check_is_same(self, other: Any) -> bool:
        if not isinstance(other, ChatGptModelTypeEntity):
            return False
        return self.key == other.key

    @classmethod
    def init_from_series(cls, series: pd.Series) -> "ChatGptModelTypeEntity":
        return cls(
            key=series["key"],
            label_en=series["label_en"],
            label_jp=series["label_jp"],
        )
