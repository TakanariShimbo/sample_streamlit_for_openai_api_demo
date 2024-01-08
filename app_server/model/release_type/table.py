from typing import List, Type

import pandas as pd

from .entity import ReleaseTypeEntity
from ..base import ColumnConfig, BaseTable


class ReleaseTypeTable(BaseTable[ReleaseTypeEntity]):
    @staticmethod
    def get_column_configs() -> List[ColumnConfig]:
        return [
            ColumnConfig(name="release_id", dtype=pd.StringDtype(), unique=True, non_null=True, auto_assigned=False),
            ColumnConfig(name="label_en", dtype=pd.StringDtype(), unique=True, non_null=True, auto_assigned=False),
            ColumnConfig(name="label_jp", dtype=pd.StringDtype(), unique=True, non_null=True, auto_assigned=False),
        ]

    @staticmethod
    def get_entiry_class() -> Type[ReleaseTypeEntity]:
        return ReleaseTypeEntity

    @staticmethod
    def get_csv_filepath() -> str:
        return "./model/release_type/data.csv"

    def convert_id_to_label_en(self, release_id: str) -> str:
        return self.get_entity(column_name="release_id", value=release_id).label_en


RELEASE_TYPE_TABLE = ReleaseTypeTable.load_from_csv()
