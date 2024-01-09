from abc import ABC, abstractmethod
from textwrap import dedent
from typing import Any, Dict, List, Literal, Generic, Optional, Tuple, TypeVar, Type

import pandas as pd
from pandas.api.extensions import ExtensionDtype
from sqlalchemy import Engine, CursorResult

from .column_config import ColumnConfig
from .config import BaseConfig


C = TypeVar("C", bound=BaseConfig)
E = TypeVar("E", bound="BaseEntity")


class BaseEntity(Generic[C], ABC):
    @staticmethod
    @abstractmethod
    def _get_config_class() -> Type[C]:
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def _check_is_same(self, other: Any) -> bool:
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

    def __eq__(self, other):
        return self._check_is_same(other=other)

    @classmethod
    def init_from_series(cls: Type[E], series: pd.Series) -> E:
        kwargs = {name: series[name] for name in cls._get_column_names(ignore_auto_assigned=False)}
        return cls(**kwargs)

    def to_dict(self, ignore_auto_assigned: bool) -> Dict[str, Any]:
        entity_dict = {}
        for name in self._get_column_names(ignore_auto_assigned=ignore_auto_assigned):
            try:
                entity_dict[name] = getattr(self, name)
            except ValueError:
                entity_dict[name] = None
        return entity_dict

    def _get_insert_sql(self) -> Tuple[str, Dict[str, Any]]:
        table_name = self._get_database_table_name()
        names = []
        values = []
        for name in self._get_column_names(ignore_auto_assigned=True):
            names.append(f"{name}")
            values.append(f":{name}")
        names_str = ", ".join(names)
        values_str = ", ".join(values)

        insert_sql = dedent(
            f"""
            INSERT INTO {table_name} ({names_str})
            VALUES ({values_str});
            """
        )
        return insert_sql, self.to_dict(ignore_auto_assigned=True)

    def save_to_database(self, database_engine: Engine, mode: Literal["insert"] = "insert") -> None:
        if mode == "insert":
            sql, params = self._get_insert_sql()
            self._execute_sql(database_engine=database_engine, sql=sql, params=params)
        else:
            raise NotImplementedError("Not implemented")