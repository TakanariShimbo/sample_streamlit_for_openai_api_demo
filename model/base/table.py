from abc import ABC, abstractmethod
from typing import List, Any, TypeVar, Generic, Type

import pandas as pd

from . import ColumnConfig
from . import BaseEntity


E = TypeVar("E", bound=BaseEntity)
T = TypeVar("T", bound="BaseTable")


class BaseTable(Generic[E], ABC):
    def __init__(self, table: pd.DataFrame) -> None:
        self._validate(table)
        self._table = table

    @classmethod
    def append_b_to_a(cls: Type[T], table_a: T, table_b: T) -> T:
        table = pd.concat([table_a._table, table_b._table], ignore_index=True)
        return cls(table)

    @classmethod
    def load_from_entity_list(cls: Type[T], entity_list: List[E]) -> T:
        entity_data_list = [entity.to_dict() for entity in entity_list]
        dtype_dict = {config.name: config.dtype for config in cls.get_column_config_list()}
        table = pd.DataFrame(entity_data_list).astype(dtype_dict)
        return cls(table)

    @classmethod
    def load_from_csv(cls: Type[T], filepath: str) -> T:
        dtype_dict = {config.name: config.dtype for config in cls.get_column_config_list()}
        table = pd.read_csv(filepath, dtype=dtype_dict)
        return cls(table)

    @classmethod
    def create_empty_table(cls: Type[T]) -> T:
        series_dict = {config.name: pd.Series(dtype=config.dtype) for config in cls.get_column_config_list()}
        table = pd.DataFrame(series_dict)
        return cls(table)

    def get_all_entities(self) -> List[E]:
        return [self.get_entiry_class().init_from_series(series=row) for _, row in self._table.iterrows()]

    def get_entity(self, column_name: str, value: Any) -> E:
        mask = self._table.loc[:, column_name] == value
        matching_entities = self._table.loc[mask, :]
        if matching_entities.empty:
            raise ValueError(f"No rows found for {column_name}={value}")
        elif matching_entities.shape[0] > 1:
            raise ValueError(f"Multiple rows found for {column_name}={value}")
        return self.get_entiry_class().init_from_series(series=matching_entities.iloc[0])

    def _validate(self, df: pd.DataFrame) -> None:
        for config in self.get_column_config_list():
            if config.unique and df[config.name].duplicated().any():
                raise ValueError(f"Column {config.name} has duplicate values")
            if config.non_null and df[config.name].isnull().any():
                raise ValueError(f"Column {config.name} has null values")

    @staticmethod
    @abstractmethod
    def get_column_config_list() -> List[ColumnConfig]:
        raise NotImplementedError("Subclasses must implement this method")

    @staticmethod
    @abstractmethod
    def get_entiry_class() -> Type[E]:
        raise NotImplementedError("Subclasses must implement this method")
