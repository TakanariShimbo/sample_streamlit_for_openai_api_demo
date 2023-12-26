from typing import Dict, Any, Tuple

import streamlit as st

from .create_form_schema import CreateFormSchema
from .component_s_states import ComponentSState
from .chat_messages_s_states import ChatMessagesSState
from ..base import BaseProcesser, BaseProcessersManager, EarlyStopProcessException
from controller import ChatMessagesManager


class CreateProcesser(BaseProcesser[None]):
    def main_process(self, inner_dict: Dict[str, Any]) -> None:
        inner_dict["chat_message_manager"] = ChatMessagesManager.init_as_new(title=inner_dict["form_schema"].title)

    def pre_process(self, outer_dict: Dict[str, Any], inner_dict: Dict[str, Any]) -> None:
        pass

    def post_process(self, outer_dict: Dict[str, Any], inner_dict: Dict[str, Any]) -> None:
        pass

    def callback_process(self, content: None, outer_dict: Dict[str, Any], inner_dict: Dict[str, Any]) -> None:
        pass


class CreateProcesserManager(BaseProcessersManager):
    def pre_process_for_starting(self, **kwargs) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        outer_dict = {}
        outer_dict["message_area"] = kwargs["message_area"]

        try:
            inner_dict = {}
            inner_dict["form_schema"] = CreateFormSchema(title=kwargs["title"])
        except:
            outer_dict["message_area"].warning("Please input form corectly.")
            raise EarlyStopProcessException()
        return outer_dict, inner_dict

    def pre_process_for_running(self, **kwargs) -> Dict[str, Any]:
        outer_dict = {}
        outer_dict["message_area"] = kwargs["message_area"]

        kwargs["message_area"].warning("RUNNING")
        return outer_dict

    def post_process(self, outer_dict: Dict[str, Any], inner_dict: Dict[str, Any]) -> None:
        outer_dict["message_area"].empty()
        ChatMessagesSState.set(value=inner_dict["chat_message_manager"])
        ComponentSState.set_chat_room_entity()