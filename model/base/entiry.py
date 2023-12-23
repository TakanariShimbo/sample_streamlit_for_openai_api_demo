from abc import ABC, abstractmethod
from typing import Any, Dict, Type, TypeVar
import pandas as pd


E = TypeVar("E", bound="BaseEntity")


class BaseEntity(ABC):
    def __eq__(self, other):
        return self.check_is_same(other=other)

    @abstractmethod
    def check_is_same(self, other: Any) -> bool:
        raise NotImplementedError("Subclasses must implement this method")
    
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        raise NotImplementedError("Subclasses must implement this method")

    @classmethod
    @abstractmethod
    def init_from_series(cls: Type[E], series: pd.Series) -> E:
        raise NotImplementedError("Subclasses must implement this method")