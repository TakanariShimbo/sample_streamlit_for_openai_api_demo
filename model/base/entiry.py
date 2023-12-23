from abc import ABC, abstractmethod
from typing import Any, Dict, List, Type, TypeVar
import pandas as pd


E = TypeVar("E", bound="BaseEntity")


class BaseEntity(ABC):
    def __eq__(self, other):
        return self.check_is_same(other=other)

    def to_dict(self) -> Dict[str, Any]:
        return {name: getattr(self, name) for name in self.get_column_name_list()}

    @classmethod
    def init_from_series(cls: Type[E], series: pd.Series) -> E:
        kwargs = {name: getattr(series, name) for name in cls.get_column_name_list()}
        return cls(**kwargs)

    @abstractmethod
    def check_is_same(self, other: Any) -> bool:
        raise NotImplementedError("Subclasses must implement this method")

    @staticmethod
    @abstractmethod
    def get_column_name_list() -> List[str]:
        raise NotImplementedError("Subclasses must implement this method")
