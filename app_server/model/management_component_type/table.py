from typing import Type

from ..base import BaseTable
from .config import ManagementComponentTypeConfig
from .entity import ManagementComponentTypeEntity


class ManagementComponentTypeTable(BaseTable[ManagementComponentTypeConfig, ManagementComponentTypeEntity]):
    @staticmethod
    def _get_config_class() -> Type[ManagementComponentTypeConfig]:
        return ManagementComponentTypeConfig

    @staticmethod
    def _get_entiry_class() -> Type[ManagementComponentTypeEntity]:
        return ManagementComponentTypeEntity

    def get_sign_in_entity(self) -> ManagementComponentTypeEntity:
        return self.get_entity(column_name="component_id", value="sign_in")

    def get_home_entity(self) -> ManagementComponentTypeEntity:
        return self.get_entity(column_name="component_id", value="home")

    def get_sign_up_entity(self) -> ManagementComponentTypeEntity:
        return self.get_entity(column_name="component_id", value="sign_up")


MANAGEMENT_COMPONENT_TYPE_TABLE = ManagementComponentTypeTable.load_from_csv()
