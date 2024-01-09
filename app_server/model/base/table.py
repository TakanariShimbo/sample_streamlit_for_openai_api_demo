from abc import ABC, abstractmethod
from textwrap import dedent
from typing import List, Any, TypeVar, Generic, Optional, Type, Literal

import pandas as pd
from sqlalchemy import Engine, text

from . import ColumnConfig
from . import BaseEntity


E = TypeVar("E", bound=BaseEntity)
T = TypeVar("T", bound="BaseTable")


class BaseTable(Generic[E], ABC):
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
        dtype_dict = {config.name: config.dtype for config in cls.get_column_configs()}
        df = pd.DataFrame(entities_data).astype(dtype_dict)
        return cls(df)

    @classmethod
    def load_from_csv(cls: Type[T], filepath: Optional[str] = None) -> T:
        if filepath == None:
            filepath = cls.get_csv_filepath()
        dtype_dict = {config.name: config.dtype for config in cls.get_column_configs()}
        df = pd.read_csv(filepath, dtype=dtype_dict)
        cls._validate_unique(df=df)
        cls._validate_non_null(df=df)
        return cls(df)

    @classmethod
    def load_from_database(cls: Type[T], database_engine: Engine, sql: Optional[str] = None) -> T:
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
        cls.execute_sqls(
            database_engine=database_engine, 
            sqls=[
                cls.get_database_table_creation_sql(table_name=cls.get_database_table_name()), 
                cls.get_database_table_creation_sql(table_name=cls.get_temp_database_table_name()),
            ]
        )

    @classmethod
    def _validate_unique(cls: Type[T], df: pd.DataFrame) -> None:
        for config in cls.get_column_configs():
            if config.unique and df[config.name].duplicated().any():
                raise ValueError(f"Column {config.name} has duplicate values")

    @classmethod
    def _validate_non_null(cls: Type[T], df: pd.DataFrame) -> None:
        for config in cls.get_column_configs():
            if config.non_null and df[config.name].isnull().any():
                raise ValueError(f"Column {config.name} has null values")

    @classmethod
    def get_temp_database_table_name(cls: Type[T]) -> str:
        return f"{cls.get_database_table_name()}_temp"

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

    def save_to_csv(self, filepath: Optional[str] = None) -> None:
        if filepath == None:
            filepath = self.get_csv_filepath()
        self._df.to_csv(filepath, index=False, mode="a")

    def save_to_database(self, database_engine: Engine, mode: Literal["insert", "upsert"] = "insert") -> None:
        if mode == "insert":
            self._insert_to_database(database_engine=database_engine)
        elif mode == "upsert":
            self._upsert_to_database(database_engine=database_engine)
        else:
            raise NotImplementedError("Not implemented")

    def _insert_to_database(self, database_engine: Engine) -> None:
        columns = [config.name for config in self.get_column_configs() if not config.auto_assigned]
        self._df.loc[:, columns].to_sql(name=self.get_database_table_name(), con=database_engine, if_exists="append", index=False)

    def _upsert_to_database(self, database_engine: Engine) -> None:
        truncate_sql = self._get_truncate_sql(table_name=self.get_temp_database_table_name())
        self.execute_sqls(database_engine=database_engine, sqls=[truncate_sql])

        columns = [config.name for config in self.get_column_configs() if not config.auto_assigned]
        self._df.loc[:, columns].to_sql(name=self.get_temp_database_table_name(), con=database_engine, if_exists="append", index=False)

        upsert_sql = self._get_upsert_sql(
            table_name=self.get_database_table_name(),
            temp_table_name=self.get_temp_database_table_name(),
            columns=columns,
        )
        self.execute_sqls(database_engine=database_engine, sqls=[upsert_sql])

    def _validate_columns(self, df: pd.DataFrame):
        columns = [config.name for config in self.get_column_configs()]
        if set(df.columns) != set(columns):
            raise ValueError("DataFrame columns do not match expected columns.")

    @staticmethod
    def execute_sqls(database_engine: Engine, sqls: List[str]) -> None:
        with database_engine.connect() as conn:
            for sql in sqls:
                conn.execute(statement=text(sql))
            conn.commit()

    @staticmethod
    def _get_truncate_sql(table_name: str) -> str:
        return f"TRUNCATE TABLE {table_name};"

    @staticmethod
    def _get_upsert_sql(table_name: str, temp_table_name: str, columns: List[str]) -> str:
        columns_str = ', '.join(columns)
        target_column = columns[0]
        update_str = ', '.join([f"{col} = EXCLUDED.{col}" for col in columns[1::]])

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
    def get_database_table_creation_sql(table_name: str) -> str:
        raise NotImplementedError("Not implemented")
