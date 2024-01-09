from abc import ABC, abstractmethod
from textwrap import dedent
from typing import Any, Dict, List, Generic, Literal, Optional, TypeVar, Type

import pandas as pd
from pandas.api.extensions import ExtensionDtype
from sqlalchemy import Engine, CursorResult

from .column_config import ColumnConfig
from .config import BaseConfig
from .entiry import BaseEntity


C = TypeVar("C", bound=BaseConfig)
E = TypeVar("E", bound=BaseEntity)
T = TypeVar("T", bound="BaseTable")


class BaseTable(Generic[C, E], ABC):    
    @staticmethod
    @abstractmethod
    def _get_config_class() -> Type[C]:
        raise NotImplementedError("Subclasses must implement this method")

    @staticmethod
    @abstractmethod
    def _get_entiry_class() -> Type[E]:
        raise NotImplementedError("Subclasses must implement this method")

    @classmethod
    def _get_column_configs(cls) -> List[ColumnConfig]:
        return cls._get_config_class()._get_column_configs()

    @classmethod
    def _get_csv_filepath(cls) -> str:
        return cls._get_config_class()._get_csv_filepath()

    @classmethod
    def _get_database_table_name(cls) -> str:
        return cls._get_config_class()._get_database_table_name()

    @classmethod
    def _get_temp_database_table_name(cls) -> str:
        return cls._get_config_class()._get_temp_database_table_name()

    @classmethod
    def _execute_sql(cls, database_engine: Engine, sql: str) -> CursorResult:
        return cls._get_config_class()._execute_sql(database_engine=database_engine, sql=sql)
    
    @classmethod
    def _execute_sqls(cls, database_engine: Engine, sqls: List[str]) -> List[CursorResult]:
        return cls._get_config_class()._execute_sqls(database_engine=database_engine, sqls=sqls)

    @classmethod
    def _get_dtype_dict(cls) -> Dict[str, ExtensionDtype]:
        return cls._get_config_class()._get_dtype_dict()

    def __init__(self, df: pd.DataFrame) -> None:
        self._validate_columns(df=df)
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
        dtype_dict = {config.name: config.dtype for config in cls._get_column_configs()}
        df = pd.DataFrame(entities_data).astype(dtype_dict)
        return cls(df)

    @classmethod
    def load_from_csv(cls: Type[T], filepath: Optional[str] = None) -> T:
        if filepath == None:
            filepath = cls._get_csv_filepath()
        dtype_dict = {config.name: config.dtype for config in cls._get_column_configs()}
        df = pd.read_csv(filepath, dtype=dtype_dict)
        cls._validate_unique(df=df)
        cls._validate_non_null(df=df)
        return cls(df)

    @classmethod
    def load_from_database(cls: Type[T], database_engine: Engine, sql: Optional[str] = None) -> T:
        if sql == None:
            table_name = cls._get_database_table_name()
            sql = f"SELECT * FROM {table_name}"
        dtype_dict = {config.name: config.dtype for config in cls._get_column_configs()}
        df = pd.read_sql_query(sql=sql, con=database_engine, dtype=dtype_dict)
        return cls(df)

    @classmethod
    def create_empty_table(cls: Type[T]) -> T:
        series_dict = {config.name: pd.Series(dtype=config.dtype) for config in cls._get_column_configs()}
        df = pd.DataFrame(series_dict)
        return cls(df)

    @classmethod
    def _validate_unique(cls: Type[T], df: pd.DataFrame) -> None:
        for config in cls._get_column_configs():
            if config.unique and df[config.name].duplicated().any():
                raise ValueError(f"Column {config.name} has duplicate values")

    @classmethod
    def _validate_non_null(cls: Type[T], df: pd.DataFrame) -> None:
        for config in cls._get_column_configs():
            if config.non_null and df[config.name].isnull().any():
                raise ValueError(f"Column {config.name} has null values")

    def get_all_entities(self) -> List[E]:
        return [self._get_entiry_class().init_from_series(series=row) for _, row in self._df.iterrows()]

    def get_entity(self, column_name: str, value: Any) -> E:
        rows_mask = self._df.loc[:, column_name] == value
        matching_df = self._df.loc[rows_mask, :]
        if matching_df.empty:
            raise ValueError(f"No rows found for {column_name}={value}")
        elif matching_df.shape[0] > 1:
            raise ValueError(f"Multiple rows found for {column_name}={value}")
        return self._get_entiry_class().init_from_series(series=matching_df.iloc[0])

    def save_to_csv(self, filepath: Optional[str] = None) -> None:
        if filepath == None:
            filepath = self._get_csv_filepath()
        self._df.to_csv(filepath, index=False, mode="a")

    def save_to_database(self, database_engine: Engine, mode: Literal["insert", "upsert"] = "insert") -> None:
        if mode == "insert":
            self._insert_to_database(database_engine=database_engine)
        elif mode == "upsert":
            self._upsert_to_database(database_engine=database_engine)
        else:
            raise NotImplementedError("Not implemented")

    def _insert_to_database(self, database_engine: Engine) -> None:
        columns = [config.name for config in self._get_column_configs() if not config.auto_assigned]
        self._df.loc[:, columns].to_sql(name=self._get_database_table_name(), con=database_engine, if_exists="append", index=False)

    def _upsert_to_database(self, database_engine: Engine) -> None:
        truncate_sql = self._get_truncate_sql(table_name=self._get_temp_database_table_name())
        self._execute_sqls(database_engine=database_engine, sqls=[truncate_sql])

        columns = [config.name for config in self._get_column_configs() if not config.auto_assigned]
        self._df.loc[:, columns].to_sql(name=self._get_temp_database_table_name(), con=database_engine, if_exists="append", index=False)

        upsert_sql = self._get_upsert_sql(
            table_name=self._get_database_table_name(),
            temp_table_name=self._get_temp_database_table_name(),
            columns=columns,
        )
        self._execute_sqls(database_engine=database_engine, sqls=[upsert_sql])

    def _validate_columns(self, df: pd.DataFrame):
        columns = [config.name for config in self._get_column_configs()]
        if set(df.columns) != set(columns):
            raise ValueError("DataFrame columns do not match expected columns.")

    @staticmethod
    def _get_truncate_sql(table_name: str) -> str:
        return f"TRUNCATE TABLE {table_name};"

    @staticmethod
    def _get_upsert_sql(table_name: str, temp_table_name: str, columns: List[str]) -> str:
        columns_str = ", ".join(columns)
        target_column = columns[0]
        update_str = ", ".join([f"{col} = EXCLUDED.{col}" for col in columns[1::]])

        upsert_sql = dedent(
            f"""
            INSERT INTO {table_name} ({columns_str})
            SELECT {columns_str}
            FROM {temp_table_name}
            ON CONFLICT ({target_column}) 
            DO UPDATE SET 
                {update_str}
            """
        )
        return upsert_sql
