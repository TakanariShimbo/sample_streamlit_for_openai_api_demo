from typing import List, Type

import pandas as pd

from .entity import ChatGptSenderEntity
from .. import ColumnConfig, BaseTable


class ChatGptSenderTable(BaseTable[ChatGptSenderEntity]):
    @staticmethod
    def get_filepath() -> str:
        return "./model/chat_gpt_sender/data.csv"

    @staticmethod
    def get_column_config_list() -> List[ColumnConfig]:
        return [
            ColumnConfig(name="key", dtype=pd.StringDtype(), unique=True, non_null=True),
            ColumnConfig(name="label_en", dtype=pd.StringDtype(), unique=True, non_null=True),
            ColumnConfig(name="label_jp", dtype=pd.StringDtype(), unique=True, non_null=True),
        ]
    
    @staticmethod
    def get_entiry_class() -> Type[ChatGptSenderEntity]:
        return ChatGptSenderEntity
