from typing import List, Type

import pandas as pd

from .entity import PageTypeEntity
from .. import ColumnConfig, BaseTable


class PageTypeTable(BaseTable[PageTypeEntity]):
    @staticmethod
    def get_column_config_list() -> List[ColumnConfig]:
        return [
            ColumnConfig(name="key", dtype=pd.StringDtype(), unique=True, non_null=True, readonly=False),
            ColumnConfig(name="label_en", dtype=pd.StringDtype(), unique=True, non_null=True, readonly=False),
            ColumnConfig(name="label_jp", dtype=pd.StringDtype(), unique=True, non_null=True, readonly=False),
        ]

    @staticmethod
    def get_entiry_class() -> Type[PageTypeEntity]:
        return PageTypeEntity

    def get_home_entity(self) -> PageTypeEntity:
        return self.get_entity(column_name="key", value="home")

    def get_chat_gpt_entity(self) -> PageTypeEntity:
        return self.get_entity(column_name="key", value="chat_gpt")


PAGE_TYPE_TABLE = PageTypeTable.load_from_csv(filepath="./model/page_type/data.csv")
