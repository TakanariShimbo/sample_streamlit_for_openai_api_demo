from typing import List, Type

import pandas as pd

from .entity import MainComponentTypeEntity
from ..base import ColumnConfig, BaseTable


class MainComponentTypeTable(BaseTable[MainComponentTypeEntity]):
    @staticmethod
    def get_column_configs() -> List[ColumnConfig]:
        return [
            ColumnConfig(name="component_id", dtype=pd.StringDtype(), unique=True, non_null=True, auto_assigned=False),
            ColumnConfig(name="label_en", dtype=pd.StringDtype(), unique=True, non_null=True, auto_assigned=False),
            ColumnConfig(name="label_jp", dtype=pd.StringDtype(), unique=True, non_null=True, auto_assigned=False),
        ]

    @staticmethod
    def get_entiry_class() -> Type[MainComponentTypeEntity]:
        return MainComponentTypeEntity

    @staticmethod
    def get_csv_filepath() -> str:
        return "./model/main_component_type/data.csv"

    def get_wake_up_entity(self) -> MainComponentTypeEntity:
        return self.get_entity(column_name="component_id", value="wake_up")

    def get_sign_in_entity(self) -> MainComponentTypeEntity:
        return self.get_entity(column_name="component_id", value="sign_in")
    
    def get_home_entity(self) -> MainComponentTypeEntity:
        return self.get_entity(column_name="component_id", value="home")

    def get_chat_room_entity(self) -> MainComponentTypeEntity:
        return self.get_entity(column_name="component_id", value="chat_room")


MAIN_COMPONENT_TYPE_TABLE = MainComponentTypeTable.load_from_csv()
