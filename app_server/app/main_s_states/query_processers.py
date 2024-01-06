from typing import Dict, Any, Tuple

import streamlit as st

from .query_form_schema import QueryFormSchema
from .account_s_states import AccountSState
from .chat_room_s_states import ChatRoomSState
from ..base import BaseProcesser, BaseProcessersManager, EarlyStopProcessException
from controller import ChatGptManager
from model import CHAT_GPT_ROLE_TYPE_TABLE


class QueryProcesser(BaseProcesser[str]):
    def main_process(self, inner_dict: Dict[str, Any]) -> None:
        inner_dict["answer"] = ChatGptManager.query_streamly_answer_and_display(
            prompt=inner_dict["form_schema"].prompt,
            model_type=inner_dict["form_schema"].chat_gpt_model_type,
            callback_func=self.add_queue,
            message_entities=inner_dict["message_entities"],
        )

    def pre_process(self, outer_dict: Dict[str, Any], inner_dict: Dict[str, Any]) -> None:
        with outer_dict["history_area"]:
            with st.chat_message(name=CHAT_GPT_ROLE_TYPE_TABLE.get_user_entity().role_id):
                st.write(inner_dict["form_schema"].prompt)
            with st.chat_message(name=CHAT_GPT_ROLE_TYPE_TABLE.get_assistant_entity().role_id):
                outer_dict["answer_area"] = st.empty()

    def post_process(self, outer_dict: Dict[str, Any], inner_dict: Dict[str, Any]) -> None:
        outer_dict["answer_area"].write(inner_dict["answer"])

    def callback_process(self, content: str, outer_dict: Dict[str, Any], inner_dict: Dict[str, Any]) -> None:
        outer_dict["answer_area"].write(content)


class QueryProcesserManager(BaseProcessersManager):
    def pre_process_for_starting(self, **kwargs) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        outer_dict = {}
        outer_dict["message_area"] = kwargs["message_area"]
        outer_dict["history_area"] = kwargs["history_area"]

        try:
            inner_dict = {}
            inner_dict["form_schema"] = QueryFormSchema.from_entity(chat_gpt_model_entity=kwargs["chat_gpt_model_entity"], prompt=kwargs["prompt"])
            inner_dict["message_entities"] = ChatRoomSState.get().get_all_message_entities()
        except:
            outer_dict["message_area"].warning("Please input form corectly.")
            raise EarlyStopProcessException()
        return outer_dict, inner_dict

    def pre_process_for_running(self, **kwargs) -> Dict[str, Any]:
        outer_dict = {}
        outer_dict["message_area"] = kwargs["message_area"]
        outer_dict["history_area"] = kwargs["history_area"]

        kwargs["message_area"].warning("Running.")
        return outer_dict

    def post_process(self, outer_dict: Dict[str, Any], inner_dict: Dict[str, Any]) -> bool:
        chat_room_manager = ChatRoomSState.get()
        chat_room_manager.add_prompt_and_answer(
            prompt=inner_dict["form_schema"].prompt,
            answer=inner_dict["answer"],
            account_id=AccountSState.get().account_id,
            assistant_id=inner_dict["form_schema"].chat_gpt_model_type,
        )
        outer_dict["message_area"].empty()
        return True
