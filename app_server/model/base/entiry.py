from abc import ABC, abstractmethod
from typing import Any, Dict, List, Generic, TypeVar, Type

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
    def _execute_sql(cls, database_engine: Engine, sql: str) -> CursorResult:
        return cls._get_config_class()._execute_sql(database_engine=database_engine, sql=sql)
    
    @classmethod
    def _execute_sqls(cls, database_engine: Engine, sqls: List[str]) -> List[CursorResult]:
        return cls._get_config_class()._execute_sqls(database_engine=database_engine, sqls=sqls)

    @classmethod
    def _get_dtype_dict(cls) -> Dict[str, ExtensionDtype]:
        return cls._get_config_class()._get_dtype_dict()

    def __eq__(self, other):
        return self._check_is_same(other=other)

    @classmethod
    def init_from_series(cls: Type[E], series: pd.Series) -> E:
        kwargs = {column_config.name: series[column_config.name] for column_config in cls._get_column_configs()}
        return cls(**kwargs)

    def to_dict(self) -> Dict[str, Any]:
        entity_dict = {}
        for column_config in self._get_column_configs():
            try:
                entity_dict[column_config.name] = getattr(self, column_config.name)
            except ValueError:
                entity_dict[column_config.name] = None
        return entity_dict
