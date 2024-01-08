from typing import List, Type

import pandas as pd

from .entity import AssistantTypeEntity
from ..base import ColumnConfig, BaseTable


class AssistantTypeTable(BaseTable[AssistantTypeEntity]):
    @staticmethod
    def get_column_configs() -> List[ColumnConfig]:
        return [
            ColumnConfig(name="assistant_id", dtype=pd.StringDtype(), unique=True, non_null=True, auto_assigned=False),
            ColumnConfig(name="label_en", dtype=pd.StringDtype(), unique=True, non_null=True, auto_assigned=False),
            ColumnConfig(name="label_jp", dtype=pd.StringDtype(), unique=True, non_null=True, auto_assigned=False),
        ]

    @staticmethod
    def get_entiry_class() -> Type[AssistantTypeEntity]:
        return AssistantTypeEntity

    @staticmethod
    def get_csv_filepath() -> str:
        return "./model/assistant_type/data.csv"


ASSISTANT_TYPE_TABLE = AssistantTypeTable.load_from_csv()
