from abc import ABC, abstractmethod
from textwrap import dedent
from typing import List, Any, TypeVar, Generic, Optional, Type

import pandas as pd
from sqlalchemy import Engine, text, TextClause

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
    def load_from_csv(cls: Type[T], filepath: Optional[str] = None) -> T:
        if filepath == None:
            filepath = cls.get_csv_filepath()
        dtype_dict = {config.name: config.dtype for config in cls.get_column_configs()}
        df = pd.read_csv(filepath, dtype=dtype_dict)
        return cls(df)

    @classmethod
    def load_from_database(cls: Type[T], database_engine: Engine, sql: Optional[str] = None):
        if sql == None:
            table_name = cls.get_database_table_name()
            sql = f"SELECT * FROM {table_name}"
        dtype_dict = {config.name: config.dtype for config in cls.get_column_configs()}
        df = pd.read_sql_query(sql=sql, con=database_engine, dtype=dtype_dict)
        return cls(df)

    @classmethod
    def create_empty_table(cls: Type[T]) -> T:
        series_dict = {config.name: pd.Series(dtype=config.dtype) for config in cls.get_column_configs()}
        df = pd.DataFrame(series_dict)
        return cls(df)
    
    @classmethod
    def create_table_on_database(cls: Type[T], database_engine: Engine) -> None:
        table_name = f"{cls.get_database_table_name()}"
        temp_table_name = f"{cls.get_database_table_name()}_temp"

        with database_engine.connect() as conn:
            conn.execute(statement=cls.get_table_creation_sql(table_name=table_name))
            conn.execute(statement=cls.get_table_creation_sql(table_name=temp_table_name))
            conn.commit()

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

    def save_to_csv(self, filepath: Optional[str] = None):
        if filepath == None:
            filepath = self.get_csv_filepath()
        self._df.to_csv(filepath, index=False, mode="a")

    def save_to_database(self, database_engine: Engine):
        table_name = self.get_database_table_name()
        columns = [config.name for config in self.get_column_configs() if not config.readonly]
        self._df.loc[:, columns].to_sql(name=table_name, con=database_engine, if_exists="append", index=False)

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

    @staticmethod
    def get_csv_filepath() -> str:
        raise NotImplementedError("Not implemented")

    @staticmethod
    def get_database_table_name() -> str:
        raise NotImplementedError("Not implemented")

    @staticmethod
    def get_table_creation_sql(table_name: str) -> TextClause:
        raise NotImplementedError("Not implemented")
