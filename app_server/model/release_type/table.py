from typing import List, Type

import pandas as pd

from .entity import ReleaseTypeEntity
from ..base import ColumnConfig, BaseTable


class ReleaseTypeTable(BaseTable[ReleaseTypeEntity]):
    @staticmethod
    def get_column_configs() -> List[ColumnConfig]:
        return [
            ColumnConfig(name="key", dtype=pd.StringDtype(), unique=True, non_null=True, readonly=False),
            ColumnConfig(name="label_en", dtype=pd.StringDtype(), unique=True, non_null=True, readonly=False),
            ColumnConfig(name="label_jp", dtype=pd.StringDtype(), unique=True, non_null=True, readonly=False),
        ]

    @staticmethod
    def get_entiry_class() -> Type[ReleaseTypeEntity]:
        return ReleaseTypeEntity

    @staticmethod
    def get_csv_filepath() -> str:
        return "./model/release_type/data.csv"


RELEASE_TYPE_TABLE = ReleaseTypeTable.load_from_csv()
