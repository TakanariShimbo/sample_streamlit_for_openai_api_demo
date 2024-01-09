from typing import Type
from sqlalchemy import Engine

from ..base import BaseTable
from .config import AccountConfig
from .entity import AccountEntity


class AccountTable(BaseTable[AccountConfig, AccountEntity]):
    @staticmethod
    def _get_config_class() -> Type[AccountConfig]:
        return AccountConfig

    @staticmethod
    def _get_entiry_class() -> Type[AccountEntity]:
        return AccountEntity

    @classmethod
    def load_specified_account_from_database(cls, database_engine: Engine, account_id: str) -> "AccountTable":
        table_name = cls._get_database_table_name()
        sql = f"SELECT * FROM {table_name} WHERE account_id = '{account_id}'"
        return cls.load_from_database(database_engine=database_engine, sql=sql)

    def get_specified_accout_entity(self, account_id: str) -> AccountEntity:
        return self.get_entity(column_name="account_id", value=account_id)
