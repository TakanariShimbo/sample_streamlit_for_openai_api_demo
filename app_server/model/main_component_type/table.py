from typing import Type

from ..base import BaseTable
from .config import MainComponentTypeConfig
from .entity import MainComponentTypeEntity


class MainComponentTypeTable(BaseTable[MainComponentTypeConfig, MainComponentTypeEntity]):
    @staticmethod
    def _get_config_class() -> Type[MainComponentTypeConfig]:
        return MainComponentTypeConfig

    @staticmethod
    def _get_entiry_class() -> Type[MainComponentTypeEntity]:
        return MainComponentTypeEntity

    def get_wake_up_entity(self) -> MainComponentTypeEntity:
        return self.get_entity(column_name="component_id", value="wake_up")

    def get_sign_in_entity(self) -> MainComponentTypeEntity:
        return self.get_entity(column_name="component_id", value="sign_in")

    def get_home_entity(self) -> MainComponentTypeEntity:
        return self.get_entity(column_name="component_id", value="home")

    def get_chat_room_entity(self) -> MainComponentTypeEntity:
        return self.get_entity(column_name="component_id", value="chat_room")


MAIN_COMPONENT_TYPE_TABLE = MainComponentTypeTable.load_from_csv()
