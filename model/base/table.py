from abc import ABC, abstractmethod
from typing import List, Dict, Any, TypeVar, Generic, Type

import pandas as pd

from . import ColumnConfig
from . import BaseEntity


E = TypeVar("E", bound=BaseEntity)
T = TypeVar("T", bound="BaseTable")


class BaseTable(Generic[E], ABC):
    def __init__(self, table: pd.DataFrame) -> None:
        self._validate(table)
        self._table = table

    def get_all_entities(self) -> List[E]:
        return [self.get_entiry_class()(series=row) for _, row in self._table.iterrows()]

    def get_entity(self, column_name: str, value: Any) -> E:
        mask = self._table.loc[:, column_name] == value
        matching_entities = self._table.loc[mask, :]
        if matching_entities.empty:
            raise ValueError(f"No rows found for {column_name}={value}")
        elif matching_entities.shape[0] > 1:
            raise ValueError(f"Multiple rows found for {column_name}={value}")
        return self.get_entiry_class()(series=matching_entities.iloc[0])

    @classmethod
    def load_from_csv(cls: Type[T], filepath: str) -> T:
        table = pd.read_csv(filepath, dtype=cls.get_dtypes())
        return cls(table)

    @classmethod
    def get_dtypes(cls) -> Dict[str, Any]:
        return {column_config.name: column_config.dtype for column_config in cls.get_column_config_list()}

    def _validate(self, df: pd.DataFrame) -> None:
        for column_config in self.get_column_config_list():
            if column_config.unique and df[column_config.name].duplicated().any():
                raise ValueError(f"Column {column_config.name} has duplicate values")
            if column_config.non_null and df[column_config.name].isnull().any():
                raise ValueError(f"Column {column_config.name} has null values")

    @staticmethod
    @abstractmethod
    def get_column_config_list() -> List[ColumnConfig]:
        raise NotImplementedError("Subclasses must implement this method")

    @staticmethod
    @abstractmethod
    def get_entiry_class() -> Type[E]:
        raise NotImplementedError("Subclasses must implement this method")
