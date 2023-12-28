from typing import List, Type

import pandas as pd

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
