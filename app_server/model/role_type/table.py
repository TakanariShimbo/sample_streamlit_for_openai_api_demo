from typing import List, Type

import pandas as pd

from .entity import RoleTypeEntity
from ..base import ColumnConfig, BaseTable


class RoleTypeTable(BaseTable[RoleTypeEntity]):
    @staticmethod
    def get_column_configs() -> List[ColumnConfig]:
        return [
            ColumnConfig(name="role_id", dtype=pd.StringDtype(), unique=True, non_null=True, readonly=False),
            ColumnConfig(name="label_en", dtype=pd.StringDtype(), unique=True, non_null=True, readonly=False),
            ColumnConfig(name="label_jp", dtype=pd.StringDtype(), unique=True, non_null=True, readonly=False),
        ]

    @staticmethod
    def get_entiry_class() -> Type[RoleTypeEntity]:
        return RoleTypeEntity

    @staticmethod
    def get_csv_filepath() -> str:
        return "./model/role_type/data.csv"

    def get_system_entity(self) -> RoleTypeEntity:
        return self.get_entity(column_name="role_id", value="system")

    def get_user_entity(self) -> RoleTypeEntity:
        return self.get_entity(column_name="role_id", value="user")
    
    def get_assistant_entity(self) -> RoleTypeEntity:
        return self.get_entity(column_name="role_id", value="assistant")


ROLE_TYPE_TABLE = RoleTypeTable.load_from_csv()
