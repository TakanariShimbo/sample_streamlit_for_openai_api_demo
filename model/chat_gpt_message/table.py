from typing import List, Type

import pandas as pd

from .entity import ChatGptMessageEntity
from .. import ColumnConfig, BaseTable


class ChatGptMessageTable(BaseTable[ChatGptMessageEntity]):
    @staticmethod
    def get_column_config_list() -> List[ColumnConfig]:
        return [
            ColumnConfig(name="role", dtype=pd.StringDtype(), unique=False, non_null=True, readonly=False),
            ColumnConfig(name="name", dtype=pd.StringDtype(), unique=False, non_null=True, readonly=False),
            ColumnConfig(name="content", dtype=pd.StringDtype(), unique=False, non_null=True, readonly=False),
        ]

    @staticmethod
    def get_entiry_class() -> Type[ChatGptMessageEntity]:
        return ChatGptMessageEntity
