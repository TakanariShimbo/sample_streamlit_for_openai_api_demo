from typing import List, Type

import pandas as pd

from .entity import ChatGptRoleTypeEntity
from ..base import ColumnConfig, BaseTable


class ChatGptRoleTypeTable(BaseTable[ChatGptRoleTypeEntity]):
    @staticmethod
    def get_column_configs() -> List[ColumnConfig]:
        return [
            ColumnConfig(name="role_id", dtype=pd.StringDtype(), unique=True, non_null=True, readonly=False),
            ColumnConfig(name="label_en", dtype=pd.StringDtype(), unique=True, non_null=True, readonly=False),
            ColumnConfig(name="label_jp", dtype=pd.StringDtype(), unique=True, non_null=True, readonly=False),
        ]

    @staticmethod
    def get_entiry_class() -> Type[ChatGptRoleTypeEntity]:
        return ChatGptRoleTypeEntity

    @staticmethod
    def get_csv_filepath() -> str:
        return "./model/chat_gpt_role_type/data.csv"

    def get_system_entity(self) -> ChatGptRoleTypeEntity:
        return self.get_entity(column_name="role_id", value="system")

    def get_user_entity(self) -> ChatGptRoleTypeEntity:
        return self.get_entity(column_name="role_id", value="user")
    
    def get_assistant_entity(self) -> ChatGptRoleTypeEntity:
        return self.get_entity(column_name="role_id", value="assistant")


CHAT_GPT_ROLE_TYPE_TABLE = ChatGptRoleTypeTable.load_from_csv()
