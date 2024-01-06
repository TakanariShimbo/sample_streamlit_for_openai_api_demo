from typing import Dict, Any, Tuple

from .main_component_s_states import MainComponentSState
from .chat_room_s_states import ChatRoomSState
from ..base import BaseProcesser, BaseProcessersManager
from controller import ChatRoomManager


class EnterProcesser(BaseProcesser[None]):
    def main_process(self, inner_dict: Dict[str, Any]) -> None:
        inner_dict["chat_message_manager"] = ChatRoomManager.init_as_continue(
            room_id=inner_dict["room_id"],
            account_id=inner_dict["account_id"],
            release_id=inner_dict["release"],
        )

    def pre_process(self, outer_dict: Dict[str, Any], inner_dict: Dict[str, Any]) -> None:
        pass

    def post_process(self, outer_dict: Dict[str, Any], inner_dict: Dict[str, Any]) -> None:
        pass

    def callback_process(self, content: None, outer_dict: Dict[str, Any], inner_dict: Dict[str, Any]) -> None:
        pass


class EnterProcesserManager(BaseProcessersManager):
    def pre_process_for_starting(self, **kwargs) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        outer_dict = {}
        inner_dict = {}
        inner_dict["room_id"] = kwargs["room_id"]
        inner_dict["account_id"] = kwargs["account_id"]
        inner_dict["release"] = kwargs["release"]
        return outer_dict, inner_dict

    def pre_process_for_running(self, **kwargs) -> Dict[str, Any]:
        outer_dict = {}
        return outer_dict

    def post_process(self, outer_dict: Dict[str, Any], inner_dict: Dict[str, Any]) -> bool:
        ChatRoomSState.set(value=inner_dict["chat_message_manager"])
        MainComponentSState.set_chat_room_entity()
        return True
