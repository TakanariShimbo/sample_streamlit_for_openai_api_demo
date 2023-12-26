from typing import List, Type

import pandas as pd

from .entity import ComponentTypeEntity
from ..base import ColumnConfig, BaseTable


class ComponentTypeTable(BaseTable[ComponentTypeEntity]):
    @staticmethod
    def get_column_configs() -> List[ColumnConfig]:
        return [
            ColumnConfig(name="key", dtype=pd.StringDtype(), unique=True, non_null=True, readonly=False),
            ColumnConfig(name="label_en", dtype=pd.StringDtype(), unique=True, non_null=True, readonly=False),
            ColumnConfig(name="label_jp", dtype=pd.StringDtype(), unique=True, non_null=True, readonly=False),
        ]

    @staticmethod
    def get_entiry_class() -> Type[ComponentTypeEntity]:
        return ComponentTypeEntity

    @staticmethod
    def get_csv_filepath() -> str:
        return "./model/component_type/data.csv"

    def get_wake_up_entity(self) -> ComponentTypeEntity:
        return self.get_entity(column_name="key", value="wake_up")

    def get_home_entity(self) -> ComponentTypeEntity:
        return self.get_entity(column_name="key", value="home")

    def get_chat_room_entity(self) -> ComponentTypeEntity:
        return self.get_entity(column_name="key", value="chat_room")


COMPONENT_TYPE_TABLE = ComponentTypeTable.load_from_csv()
