from abc import ABC, abstractmethod
from typing import Dict, List

from pandas.api.extensions import ExtensionDtype
from sqlalchemy import Engine, text, CursorResult

from . import ColumnConfig


class BaseConfig(ABC):
    @staticmethod
    @abstractmethod
    def _get_column_configs() -> List[ColumnConfig]:
        raise NotImplementedError("Subclasses must implement this method")

    @staticmethod
    def _get_database_table_name() -> str:
        raise NotImplementedError("Not implemented")

    @staticmethod
    def _get_database_table_creation_sql(table_name: str) -> str:
        raise NotImplementedError("Not implemented")

    @staticmethod
    def _get_csv_filepath() -> str:
        raise NotImplementedError("Not implemented")

    @staticmethod
    def _execute_sql(database_engine: Engine, sql: str) -> CursorResult:
        with database_engine.connect() as conn:
            result = conn.execute(statement=text(sql))
            conn.commit()
        return result

    @staticmethod
    def _execute_sqls(database_engine: Engine, sqls: List[str]) -> List[CursorResult]:
        results = []
        with database_engine.connect() as conn:
            for sql in sqls:
                result = conn.execute(statement=text(sql))
                results.append(result)
            conn.commit()
        return results

    
    @classmethod
    def _get_column_names(cls, ignore_auto_assigned: bool) -> List[str]:
        if ignore_auto_assigned:
            return [config.name for config in cls._get_column_configs() if not config.auto_assigned]
        else:
            return [config.name for config in cls._get_column_configs()]

    @classmethod
    def _get_dtype_dict(cls) -> Dict[str, ExtensionDtype]:
        return {config.name: config.dtype for config in cls._get_column_configs()}

    @classmethod
    def _get_temp_database_table_name(cls) -> str:
        return f"{cls._get_database_table_name()}_temp"

    @classmethod
    def create_table_on_database(cls, database_engine: Engine) -> None:
        cls._execute_sqls(
            database_engine=database_engine,
            sqls=[
                cls._get_database_table_creation_sql(table_name=cls._get_database_table_name()),
                cls._get_database_table_creation_sql(table_name=cls._get_temp_database_table_name()),
            ],
        )
