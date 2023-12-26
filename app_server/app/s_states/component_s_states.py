from ..base import BaseSState
from model import COMPONENT_TYPE_TABLE, ComponentTypeEntity


class ComponentSState(BaseSState[ComponentTypeEntity]):
    @staticmethod
    def get_name() -> str:
        return "CHAT_ROOM_MANAGER"

    @staticmethod
    def get_default() -> ComponentTypeEntity:
        return COMPONENT_TYPE_TABLE.get_wake_up_entity()

    @classmethod
    def set_home_entity(cls):
        cls.set(value=COMPONENT_TYPE_TABLE.get_home_entity())

    @classmethod
    def set_chat_room_entity(cls):
        cls.set(value=COMPONENT_TYPE_TABLE.get_chat_room_entity())
