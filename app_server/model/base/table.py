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
    def _execute_sql(cls, database_engine: Engine, sql: str, params: Optional[Dict[str, Any]] = None) -> CursorResult:
        return cls._get_config_class()._execute_sql(database_engine=database_engine, sql=sql, params=params)
    
    @classmethod
    def _execute_sqls(cls, database_engine: Engine, sqls: List[str]) -> List[CursorResult]:
        return cls._get_config_class()._execute_sqls(database_engine=database_engine, sqls=sqls)

    @classmethod
    def _get_column_names(cls, ignore_auto_assigned: bool) -> List[str]:
        return cls._get_config_class()._get_column_names(ignore_auto_assigned=ignore_auto_assigned)

    @classmethod
    def _get_dtype_dict(cls) -> Dict[str, ExtensionDtype]:
        return cls._get_config_class()._get_dtype_dict()

    def __init__(self, df: pd.DataFrame) -> None:
        self._validate_column_names(df=df)
        self._df = df

    def _validate_column_names(self, df: pd.DataFrame):
        if set(df.columns) != set(self._get_column_names(ignore_auto_assigned=False)):
            raise ValueError("DataFrame columns do not match expected columns.")

    @property
    def df(self) -> pd.DataFrame:
        return self._df

    @classmethod
    def append_b_to_a(cls: Type[T], table_a: T, table_b: T) -> T:
        df = pd.concat([table_a.df, table_b.df], ignore_index=True)
        return cls(df)

    @classmethod
    def load_from_entities(cls: Type[T], entities: List[E]) -> T:
        entities_data = [entity.to_dict(ignore_auto_assigned=False) for entity in entities]
        df = pd.DataFrame(entities_data).astype(cls._get_dtype_dict())
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

    @classmethod
    def load_from_csv(cls: Type[T], filepath: Optional[str] = None) -> T:
        if filepath == None:
            filepath = cls._get_csv_filepath()
        df = pd.read_csv(filepath, dtype=cls._get_dtype_dict())
        cls._validate_unique(df=df)
        cls._validate_non_null(df=df)
        return cls(df)

    @classmethod
    def load_from_database(cls: Type[T], database_engine: Engine, sql: Optional[str] = None) -> T:
        if sql == None:
            table_name = cls._get_database_table_name()
            sql = f"SELECT * FROM {table_name}"
        df = pd.read_sql_query(sql=sql, con=database_engine, dtype=cls._get_dtype_dict())
        return cls(df)

    @classmethod
    def create_empty_table(cls: Type[T]) -> T:
        series_dict = {name: pd.Series(dtype=dtype) for name, dtype in cls._get_dtype_dict().items()}
        df = pd.DataFrame(series_dict)
        return cls(df)

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

    @classmethod
    def _get_truncate_temp_sql(cls) -> str:
        temp_table_name = cls._get_temp_database_table_name()
        return f"TRUNCATE TABLE {temp_table_name};"

    @classmethod
    def _get_upsert_sql(cls) -> str:
        table_name = cls._get_database_table_name()
        temp_table_name = cls._get_temp_database_table_name()
        column_names = cls._get_column_names(ignore_auto_assigned=True)

        key_column_name = column_names[0]
        column_names_str = ", ".join(column_names)
        update_column_names_str = ", ".join([f"{col} = EXCLUDED.{col}" for col in column_names[1::]])

        upsert_sql = dedent(
            f"""
            INSERT INTO {table_name} ({column_names_str})
            SELECT {column_names_str}
            FROM {temp_table_name}
            ON CONFLICT ({key_column_name}) 
            DO UPDATE SET 
                {update_column_names_str}
            """
        )
        return upsert_sql

    def _insert_to_database(self, database_engine: Engine) -> None:
        column_names = self._get_column_names(ignore_auto_assigned=True)
        self._df.loc[:, column_names].to_sql(name=self._get_database_table_name(), con=database_engine, if_exists="append", index=False)

    def _upsert_to_database(self, database_engine: Engine) -> None:
        self._execute_sql(database_engine=database_engine, sql=self._get_truncate_temp_sql())

        column_names = self._get_column_names(ignore_auto_assigned=True)
        self._df.loc[:, column_names].to_sql(name=self._get_temp_database_table_name(), con=database_engine, if_exists="append", index=False)

        self._execute_sql(database_engine=database_engine, sql=self._get_upsert_sql())

    def save_to_database(self, database_engine: Engine, mode: Literal["insert", "upsert"] = "insert") -> None:
        if mode == "insert":
            self._insert_to_database(database_engine=database_engine)
        elif mode == "upsert":
            self._upsert_to_database(database_engine=database_engine)
        else:
            raise NotImplementedError("Not implemented")

    def save_to_csv(self, filepath: Optional[str] = None) -> None:
        if filepath == None:
            filepath = self._get_csv_filepath()
        self._df.to_csv(filepath, index=False, mode="a")