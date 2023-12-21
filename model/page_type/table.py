from typing import List, Type

import pandas as pd

from .entity import PageTypeEntity
from .. import ColumnConfig, BaseTable


class PageTypeTable(BaseTable[PageTypeEntity]):
    @staticmethod
    def get_filepath() -> str:
        return "./model/page_type/data.csv"

    @staticmethod
    def get_column_config_list() -> List[ColumnConfig]:
        return [
            ColumnConfig(name="key", dtype=pd.StringDtype(), unique=True, non_null=True),
            ColumnConfig(name="label_en", dtype=pd.StringDtype(), unique=True, non_null=True),
            ColumnConfig(name="label_jp", dtype=pd.StringDtype(), unique=True, non_null=True),
        ]

    @staticmethod
    def get_entiry_class() -> Type[PageTypeEntity]:
        return PageTypeEntity

    @classmethod
    def get_home_entity(cls) -> PageTypeEntity:
        return cls.get_entity(column_name="key", value="home")

    @classmethod
    def get_chat_gpt_entity(cls) -> PageTypeEntity:
        return cls.get_entity(column_name="key", value="chat_gpt")
