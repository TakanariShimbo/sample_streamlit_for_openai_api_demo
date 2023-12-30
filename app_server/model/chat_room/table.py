from typing import List, Type

import pandas as pd
from sqlalchemy import Engine

from .entity import ChatRoomEntity
from ..base import ColumnConfig, BaseTable


class ChatRoomTable(BaseTable[ChatRoomEntity]):
    @staticmethod
    def get_column_configs() -> List[ColumnConfig]:
        return [
            ColumnConfig(name="room_id", dtype=pd.StringDtype(), unique=True, non_null=True, readonly=False),
            ColumnConfig(name="account_id", dtype=pd.StringDtype(), unique=True, non_null=True, readonly=False),
            ColumnConfig(name="title", dtype=pd.StringDtype(), unique=False, non_null=True, readonly=False),
            ColumnConfig(name="created_at", dtype=pd.StringDtype(), unique=False, non_null=False, readonly=True),
        ]

    @staticmethod
    def get_entiry_class() -> Type[ChatRoomEntity]:
        return ChatRoomEntity

    @staticmethod
    def get_database_table_name() -> str:
        return "chat_rooms"

    @classmethod
    def load_rooms_including_specified_account_from_database(cls, database_engine: Engine, account_id: str, limit: int = 5) -> "ChatRoomTable":
        table_name = cls.get_database_table_name()
        sql = f"SELECT * FROM {table_name} WHERE account_id = '{account_id}' ORDER BY created_at DESC LIMIT {limit}"
        return cls.load_from_database(database_engine=database_engine, sql=sql)

    @classmethod
    def load_rooms_excluding_specified_account_from_database(cls, database_engine: Engine, account_id: str, limit: int = 5) -> "ChatRoomTable":
        table_name = cls.get_database_table_name()
        sql = f"SELECT * FROM {table_name} WHERE account_id != '{account_id}' ORDER BY created_at DESC LIMIT {limit}"
        return cls.load_from_database(database_engine=database_engine, sql=sql)
