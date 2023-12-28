from typing import Dict, Any, Tuple

from .component_s_states import ComponentSState
from .chat_messages_s_states import ChatMessagesSState
from ..base import BaseProcesser, BaseProcessersManager
from controller import ChatMessagesManager


class EnterProcesser(BaseProcesser[None]):
    def main_process(self, inner_dict: Dict[str, Any]) -> None:
        inner_dict["chat_message_manager"] = ChatMessagesManager.init_as_continue(room_id=inner_dict["room_id"])

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
        return outer_dict, inner_dict

    def pre_process_for_running(self, **kwargs) -> Dict[str, Any]:
        outer_dict = {}
        return outer_dict

    def post_process(self, outer_dict: Dict[str, Any], inner_dict: Dict[str, Any]) -> None:
        ChatMessagesSState.set(value=inner_dict["chat_message_manager"])
        ComponentSState.set_chat_room_entity()