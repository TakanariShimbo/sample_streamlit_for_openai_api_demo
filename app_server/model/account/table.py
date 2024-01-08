from typing import List, Type
from textwrap import dedent

import pandas as pd
from sqlalchemy import Engine

from .entity import AccountEntity
from ..base import ColumnConfig, BaseTable


class AccountTable(BaseTable[AccountEntity]):
    @staticmethod
    def get_column_configs() -> List[ColumnConfig]:
        return [
            ColumnConfig(name="account_id", dtype=pd.StringDtype(), unique=True, non_null=True, readonly=False),
            ColumnConfig(name="hashed_password", dtype=pd.StringDtype(), unique=False, non_null=True, readonly=False),
            ColumnConfig(name="registered_at", dtype=pd.StringDtype(), unique=False, non_null=False, readonly=True),
        ]

    @staticmethod
    def get_entiry_class() -> Type[AccountEntity]:
        return AccountEntity

    @staticmethod
    def get_database_table_name() -> str:
        return "accounts"

    @staticmethod
    def get_table_creation_sql(table_name: str) -> str:
        return dedent(
            f"""
            CREATE TABLE {table_name} (
                account_id VARCHAR(255) PRIMARY KEY,
                hashed_password VARCHAR(255) NOT NULL,
                registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
        )

    @classmethod
    def load_specified_account_from_database(cls, database_engine: Engine, account_id: str) -> "AccountTable":
        table_name = cls.get_database_table_name()
        sql = f"SELECT * FROM {table_name} WHERE account_id = '{account_id}'"
        return cls.load_from_database(database_engine=database_engine, sql=sql)

    def get_specified_accout_entity(self, account_id: str) -> AccountEntity:
        return self.get_entity(column_name="account_id", value=account_id)
