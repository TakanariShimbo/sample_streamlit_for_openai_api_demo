from typing import List, Type

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
