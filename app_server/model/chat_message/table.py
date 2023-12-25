from typing import List, Optional, Type

import pandas as pd
from sqlalchemy import Engine

from .entity import ChatMessageEntity
from ..base import ColumnConfig, BaseTable


class ChatMessageTable(BaseTable[ChatMessageEntity]):
    @staticmethod
    def get_column_configs() -> List[ColumnConfig]:
        return [
            ColumnConfig(name="room_id", dtype=pd.StringDtype(), unique=False, non_null=True, readonly=False),
            ColumnConfig(name="role", dtype=pd.StringDtype(), unique=False, non_null=True, readonly=False),
            ColumnConfig(name="sender_id", dtype=pd.StringDtype(), unique=False, non_null=True, readonly=False),
            ColumnConfig(name="content", dtype=pd.StringDtype(), unique=False, non_null=True, readonly=False),
        ]

    @staticmethod
    def get_entiry_class() -> Type[ChatMessageEntity]:
        return ChatMessageEntity

    @staticmethod
    def get_database_table_name() -> str:
        return "chat_messages"
    
    @classmethod
    def load_specified_room_from_database(cls, database_engine: Engine, room_id: str) -> "ChatMessageTable":
        table_name = cls.get_database_table_name()
        sql = f"SELECT * FROM {table_name} WHERE room_id = {room_id}"
        return cls.load_from_database(database_engine=database_engine, sql=sql)
