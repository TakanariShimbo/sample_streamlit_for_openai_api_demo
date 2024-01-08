from typing import List, Type

import pandas as pd

from .entity import ManagementComponentTypeEntity
from ..base import ColumnConfig, BaseTable


class ManagementComponentTypeTable(BaseTable[ManagementComponentTypeEntity]):
    @staticmethod
    def get_column_configs() -> List[ColumnConfig]:
        return [
            ColumnConfig(name="component_id", dtype=pd.StringDtype(), unique=True, non_null=True, auto_assigned=False),
            ColumnConfig(name="label_en", dtype=pd.StringDtype(), unique=True, non_null=True, auto_assigned=False),
            ColumnConfig(name="label_jp", dtype=pd.StringDtype(), unique=True, non_null=True, auto_assigned=False),
        ]

    @staticmethod
    def get_entiry_class() -> Type[ManagementComponentTypeEntity]:
        return ManagementComponentTypeEntity

    @staticmethod
    def get_csv_filepath() -> str:
        return "./model/management_component_type/data.csv"

    def get_sign_in_entity(self) -> ManagementComponentTypeEntity:
        return self.get_entity(column_name="component_id", value="sign_in")
    
    def get_home_entity(self) -> ManagementComponentTypeEntity:
        return self.get_entity(column_name="component_id", value="home")
    
    def get_sign_up_entity(self) -> ManagementComponentTypeEntity:
        return self.get_entity(column_name="component_id", value="sign_up")


MANAGEMENT_COMPONENT_TYPE_TABLE = ManagementComponentTypeTable.load_from_csv()
