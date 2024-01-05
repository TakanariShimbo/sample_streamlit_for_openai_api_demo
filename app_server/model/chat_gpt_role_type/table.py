from typing import List, Type

import pandas as pd

from .entity import ChatGptRoleTypeEntity
from ..base import ColumnConfig, BaseTable


class ChatGptRoleTypeTable(BaseTable[ChatGptRoleTypeEntity]):
    @staticmethod
    def get_column_configs() -> List[ColumnConfig]:
        return [
            ColumnConfig(name="key", dtype=pd.StringDtype(), unique=True, non_null=True, readonly=False),
            ColumnConfig(name="label_en", dtype=pd.StringDtype(), unique=True, non_null=True, readonly=False),
            ColumnConfig(name="label_jp", dtype=pd.StringDtype(), unique=True, non_null=True, readonly=False),
        ]

    @staticmethod
    def get_entiry_class() -> Type[ChatGptRoleTypeEntity]:
        return ChatGptRoleTypeEntity

    @staticmethod
    def get_csv_filepath() -> str:
        return "./model/chat_gpt_role_type/data.csv"


CHAT_GPT_ROLE_TYPE_TABLE = ChatGptRoleTypeTable.load_from_csv()
