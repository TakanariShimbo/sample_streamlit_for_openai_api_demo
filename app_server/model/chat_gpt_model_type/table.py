from typing import List, Type

import pandas as pd

from .entity import ChatGptModelTypeEntity
from ..base import ColumnConfig, BaseTable


class ChatGptModelTypeTable(BaseTable[ChatGptModelTypeEntity]):
    @staticmethod
    def get_column_configs() -> List[ColumnConfig]:
        return [
            ColumnConfig(name="assistant_id", dtype=pd.StringDtype(), unique=True, non_null=True, readonly=False),
            ColumnConfig(name="label_en", dtype=pd.StringDtype(), unique=True, non_null=True, readonly=False),
            ColumnConfig(name="label_jp", dtype=pd.StringDtype(), unique=True, non_null=True, readonly=False),
        ]

    @staticmethod
    def get_entiry_class() -> Type[ChatGptModelTypeEntity]:
        return ChatGptModelTypeEntity

    @staticmethod
    def get_csv_filepath() -> str:
        return "./model/chat_gpt_model_type/data.csv"


CHAT_GPT_MODEL_TYPE_TABLE = ChatGptModelTypeTable.load_from_csv()
