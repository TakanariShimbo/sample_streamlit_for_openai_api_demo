from typing import Type

from ..base import BaseTable
from .config import RoleTypeConfig
from .entity import RoleTypeEntity


class RoleTypeTable(BaseTable[RoleTypeConfig, RoleTypeEntity]):
    @staticmethod
    def _get_config_class() -> Type[RoleTypeConfig]:
        return RoleTypeConfig
    
    @staticmethod
    def _get_entiry_class() -> Type[RoleTypeEntity]:
        return RoleTypeEntity

    def get_system_entity(self) -> RoleTypeEntity:
        return self.get_entity(column_name="role_id", value="system")

    def get_user_entity(self) -> RoleTypeEntity:
        return self.get_entity(column_name="role_id", value="user")
    
    def get_assistant_entity(self) -> RoleTypeEntity:
        return self.get_entity(column_name="role_id", value="assistant")


ROLE_TYPE_TABLE = RoleTypeTable.load_from_csv()
