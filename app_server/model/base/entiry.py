from abc import ABC, abstractmethod
from typing import Any, Dict, List, Type, TypeVar
import pandas as pd


E = TypeVar("E", bound="BaseEntity")


class BaseEntity(ABC):
    def __eq__(self, other):
        return self.check_is_same(other=other)

    def to_dict(self) -> Dict[str, Any]:
        entity_dict = {}
        for name in self.get_columns():
            try:
                entity_dict[name] = getattr(self, name)
            except ValueError:
                entity_dict[name] = None
        return entity_dict

    @classmethod
    def init_from_series(cls: Type[E], series: pd.Series) -> E:
        kwargs = {name: series[name] for name in cls.get_columns()}
        return cls(**kwargs)

    @abstractmethod
    def check_is_same(self, other: Any) -> bool:
        raise NotImplementedError("Subclasses must implement this method")

    @staticmethod
    @abstractmethod
    def get_columns() -> List[str]:
        raise NotImplementedError("Subclasses must implement this method")
