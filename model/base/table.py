from abc import ABC, abstractmethod
from typing import List, Any, TypeVar, Generic, Type

import pandas as pd

from . import ColumnConfig
from . import BaseEntity


E = TypeVar("E", bound=BaseEntity)
T = TypeVar("T", bound="BaseTable")


class BaseTable(Generic[E], ABC):
    def __init__(self, df: pd.DataFrame) -> None:
        self._validate(df)
        self._df = df

    @property
    def df(self) -> pd.DataFrame:
        return self._df

    @classmethod
    def append_b_to_a(cls: Type[T], table_a: T, table_b: T) -> T:
        df = pd.concat([table_a.df, table_b.df], ignore_index=True)
        return cls(df)

    @classmethod
    def load_from_entities(cls: Type[T], entities: List[E]) -> T:
        entities_data = [entity.to_dict() for entity in entities]
        dtype_dict = {config.name: config.dtype for config in cls.get_column_configs()}
        df = pd.DataFrame(entities_data).astype(dtype_dict)
        return cls(df)

    @classmethod
    def load_from_csv(cls: Type[T], filepath: str) -> T:
        dtype_dict = {config.name: config.dtype for config in cls.get_column_configs()}
        df = pd.read_csv(filepath, dtype=dtype_dict)
        return cls(df)

    @classmethod
    def create_empty_table(cls: Type[T]) -> T:
        series_dict = {config.name: pd.Series(dtype=config.dtype) for config in cls.get_column_configs()}
        df = pd.DataFrame(series_dict)
        return cls(df)

    def get_all_entities(self) -> List[E]:
        return [self.get_entiry_class().init_from_series(series=row) for _, row in self._df.iterrows()]

    def get_entity(self, column_name: str, value: Any) -> E:
        rows_mask = self._df.loc[:, column_name] == value
        matching_df = self._df.loc[rows_mask, :]
        if matching_df.empty:
            raise ValueError(f"No rows found for {column_name}={value}")
        elif matching_df.shape[0] > 1:
            raise ValueError(f"Multiple rows found for {column_name}={value}")
        return self.get_entiry_class().init_from_series(series=matching_df.iloc[0])

    def _validate(self, df: pd.DataFrame) -> None:
        for config in self.get_column_configs():
            if config.unique and df[config.name].duplicated().any():
                raise ValueError(f"Column {config.name} has duplicate values")
            if config.non_null and df[config.name].isnull().any():
                raise ValueError(f"Column {config.name} has null values")

    @staticmethod
    @abstractmethod
    def get_column_configs() -> List[ColumnConfig]:
        raise NotImplementedError("Subclasses must implement this method")

    @staticmethod
    @abstractmethod
    def get_entiry_class() -> Type[E]:
        raise NotImplementedError("Subclasses must implement this method")
