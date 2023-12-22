from typing import List, Type

import pandas as pd

from .entity import ChatGptModelTypeEntity
from .. import ColumnConfig, BaseTable


class ChatGptModelTypeTable(BaseTable[ChatGptModelTypeEntity]):
    @staticmethod
    def get_column_config_list() -> List[ColumnConfig]:
        return [
            ColumnConfig(name="key", dtype=pd.StringDtype(), unique=True, non_null=True),
            ColumnConfig(name="label_en", dtype=pd.StringDtype(), unique=True, non_null=True),
            ColumnConfig(name="label_jp", dtype=pd.StringDtype(), unique=True, non_null=True),
        ]

    @staticmethod
    def get_entiry_class() -> Type[ChatGptModelTypeEntity]:
        return ChatGptModelTypeEntity


CHAT_GPT_MODEL_TYPE_TABLE = ChatGptModelTypeTable.load_from_csv(filepath="./model/chat_gpt_model_type/data.csv")
