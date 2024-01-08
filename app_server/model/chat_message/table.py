from textwrap import dedent
from typing import List, Type

import pandas as pd
from sqlalchemy import Engine, text, TextClause

from .entity import ChatMessageEntity
from ..base import ColumnConfig, BaseTable


class ChatMessageTable(BaseTable[ChatMessageEntity]):
    @staticmethod
    def get_column_configs() -> List[ColumnConfig]:
        return [
            ColumnConfig(name="room_id", dtype=pd.StringDtype(), unique=False, non_null=True, readonly=False),
            ColumnConfig(name="sender_id", dtype=pd.StringDtype(), unique=False, non_null=True, readonly=False),
            ColumnConfig(name="role_id", dtype=pd.StringDtype(), unique=False, non_null=True, readonly=False),
            ColumnConfig(name="content", dtype=pd.StringDtype(), unique=False, non_null=True, readonly=False),
            ColumnConfig(name="sent_at", dtype=pd.StringDtype(), unique=False, non_null=False, readonly=True),
        ]

    @staticmethod
    def get_entiry_class() -> Type[ChatMessageEntity]:
        return ChatMessageEntity

    @staticmethod
    def get_database_table_name() -> str:
        return "chat_messages"

    @staticmethod
    def get_table_creation_sql(table_name: str) -> TextClause:
        return text(
            dedent(
                f"""
                CREATE TABLE {table_name} (
                    message_serial SERIAL PRIMARY KEY,
                    room_id VARCHAR(255) NOT NULL,
                    sender_id VARCHAR(255) NOT NULL,
                    role_id VARCHAR(255) NOT NULL,
                    content TEXT NOT NULL,
                    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (room_id) REFERENCES chat_rooms (room_id) ON DELETE CASCADE
                );
                """
            )
        )

    @classmethod
    def load_messages_specified_room_from_database(cls, database_engine: Engine, room_id: str) -> "ChatMessageTable":
        table_name = cls.get_database_table_name()
        sql = f"SELECT * FROM {table_name} WHERE room_id = '{room_id}'"
        return cls.load_from_database(database_engine=database_engine, sql=sql)
