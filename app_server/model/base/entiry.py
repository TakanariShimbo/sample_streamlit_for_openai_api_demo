from abc import ABC, abstractmethod
from typing import Any, Dict, List, Type, TypeVar
import pandas as pd


E = TypeVar("E", bound="BaseEntity")


class BaseEntity(ABC):
    def __eq__(self, other):
        return self.check_is_same(other=other)

    def to_dict(self, for_saving=True) -> Dict[str, Any]:
        if for_saving:
            columns = self.get_saving_columns()
        else:
            columns = self.get_loading_columns()
        return {name: getattr(self, name) for name in columns}

    @classmethod
    def init_from_series(cls: Type[E], series: pd.Series) -> E:
        kwargs = {name: series[name] for name in cls.get_loading_columns()}
        return cls(**kwargs)

    @abstractmethod
    def check_is_same(self, other: Any) -> bool:
        raise NotImplementedError("Subclasses must implement this method")

    @staticmethod
    @abstractmethod
    def get_loading_columns() -> List[str]:
        raise NotImplementedError("Subclasses must implement this method")

    @staticmethod
    def get_saving_columns() -> List[str]:
        raise NotImplementedError("Subclasses must implement this method")
