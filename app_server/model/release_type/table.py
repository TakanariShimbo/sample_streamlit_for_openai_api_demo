from typing import List, Type

from ..base import BaseTable
from .config import ReleaseTypeConfig
from .entity import ReleaseTypeEntity


class ReleaseTypeTable(BaseTable[ReleaseTypeConfig, ReleaseTypeEntity]):
    @staticmethod
    def _get_config_class() -> Type[ReleaseTypeConfig]:
        return ReleaseTypeConfig
    
    @staticmethod
    def _get_entiry_class() -> Type[ReleaseTypeEntity]:
        return ReleaseTypeEntity

    def convert_id_to_label_en(self, release_id: str) -> str:
        return self.get_entity(column_name="release_id", value=release_id).label_en


RELEASE_TYPE_TABLE = ReleaseTypeTable.load_from_csv()
