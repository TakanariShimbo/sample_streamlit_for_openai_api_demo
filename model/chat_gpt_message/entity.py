from typing import Any

import pandas as pd

from .. import BaseEntity


class ChatGptMessageEntity(BaseEntity):
    def __init__(self, role: str, name: str, content: str) -> None:
        self._role = role
        self._name = name
        self._content = content

    @property
    def role(self) -> str:
        return self._role

    @property
    def name(self) -> str:
        return self._name

    @property
    def content(self) -> str:
        return self._content

    def check_is_same(self, other: Any) -> bool:
        return False

    @classmethod
    def init_from_series(cls, series: pd.Series) -> "ChatGptMessageEntity":
        return cls(
            role=series["role"],
            name=series["name"],
            content=series["content"],
        )
