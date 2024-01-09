from typing import Type

from sqlalchemy import Engine

from ..base import BaseTable
from .config import ChatRoomConfig
from .entity import ChatRoomEntity


class ChatRoomTable(BaseTable[ChatRoomConfig, ChatRoomEntity]):
    @staticmethod
    def _get_config_class() -> Type[ChatRoomConfig]:
        return ChatRoomConfig

    @staticmethod
    def _get_entiry_class() -> Type[ChatRoomEntity]:
        return ChatRoomEntity

    @classmethod
    def load_rooms_with_specified_account_from_database(cls, database_engine: Engine, account_id: str, limit: int = 5) -> "ChatRoomTable":
        table_name = cls._get_database_table_name()
        sql = f"SELECT * FROM {table_name} WHERE account_id = '{account_id}' ORDER BY created_at DESC LIMIT {limit}"
        return cls.load_from_database(database_engine=database_engine, sql=sql)

    @classmethod
    def load_public_rooms_without_specified_account_from_database(cls, database_engine: Engine, account_id: str, limit: int = 5) -> "ChatRoomTable":
        table_name = cls._get_database_table_name()
        sql = f"SELECT * FROM {table_name} WHERE release_id = 'public' AND account_id != '{account_id}' ORDER BY created_at DESC LIMIT {limit}"
        return cls.load_from_database(database_engine=database_engine, sql=sql)

    @classmethod
    def load_specified_room_from_database(cls, database_engine: Engine, room_id: str) -> "ChatRoomTable":
        table_name = cls._get_database_table_name()
        sql = f"SELECT * FROM {table_name} WHERE room_id = '{room_id}'"
        return cls.load_from_database(database_engine=database_engine, sql=sql)
