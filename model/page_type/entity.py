from typing import Any

import pandas as pd

from .. import BaseEntity


class PageTypeEntity(BaseEntity):
    def __init__(self, series: pd.Series):
        self.__key = series["key"]
        self.__label_en = series["label_en"]
        self.__label_jp = series["label_jp"]

    @property
    def key(self) -> str:
        return self.__key

    @property
    def label_en(self) -> str:
        return self.__label_en

    @property
    def label_jp(self) -> str:
        return self.__label_jp

    def check_is_same_instance(self, other: Any) -> bool:
        if not isinstance(other, PageTypeEntity):
            return False
        return self.key == other.key
