from typing import Type

from sqlalchemy import Engine

from ..base import BaseTable
from .config import ChatMessageConfig
from .entity import ChatMessageEntity


class ChatMessageTable(BaseTable[ChatMessageConfig, ChatMessageEntity]):
    @staticmethod
    def _get_config_class() -> Type[ChatMessageConfig]:
        return ChatMessageConfig

    @staticmethod
    def _get_entiry_class() -> Type[ChatMessageEntity]:
        return ChatMessageEntity

    @classmethod
    def load_messages_specified_room_from_database(cls, database_engine: Engine, room_id: str) -> "ChatMessageTable":
        table_name = cls._get_database_table_name()
        sql = f"SELECT * FROM {table_name} WHERE room_id = '{room_id}'"
        return cls.load_from_database(database_engine=database_engine, sql=sql)
