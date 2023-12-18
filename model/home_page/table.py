from typing import List, Type

import pandas as pd

from .entity import HomePageEntity
from .. import ColumnConfig, BaseTable


class HomePageTable(BaseTable[HomePageEntity]):
    @staticmethod
    def get_filepath() -> str:
        return "./model/home_page/data.csv"

    @staticmethod
    def get_column_config_list() -> List[ColumnConfig]:
        return [
            ColumnConfig(name="key", dtype=pd.StringDtype(), unique=True, non_null=True),
            ColumnConfig(name="label_en", dtype=pd.StringDtype(), unique=True, non_null=True),
            ColumnConfig(name="label_jp", dtype=pd.StringDtype(), unique=True, non_null=True),
        ]

    @staticmethod
    def get_entiry_class() -> Type[HomePageEntity]:
        return HomePageEntity

    @classmethod
    def get_home_entity(cls) -> HomePageEntity:
        return cls.get_entity(column_name="key", value="home")

    @classmethod
    def get_chat_gpt_entity(cls) -> HomePageEntity:
        return cls.get_entity(column_name="key", value="chat_gpt")
