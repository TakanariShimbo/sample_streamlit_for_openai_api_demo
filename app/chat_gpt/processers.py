from typing import Dict, Any, Tuple

import streamlit as st

from .schema import FormSchema
from .. import BaseProcesser, BaseProcessersManager, EarlyStopProcessException
from model import DEFAULT_OPENAI_API_KEY
from handler import ChatGptHandler


class MainProcesser(BaseProcesser[str]):
    def main_process(self, inner_dict: Dict[str, Any]) -> None:
        client = ChatGptHandler.generate_client(api_key=DEFAULT_OPENAI_API_KEY)
        inner_dict["answer"] = ChatGptHandler.query_streamly_answer_and_display(
            client=client,
            prompt=inner_dict["form_schema"].prompt,
            model_type=inner_dict["form_schema"].chat_gpt_model_type,
            callback_func=self.add_queue,
        )

    def pre_process(self, outer_dict: Dict[str, Any], inner_dict: Dict[str, Any]) -> None:
        with outer_dict["history_area"]:
            with st.chat_message(name="user"):
                st.write(inner_dict["form_schema"].prompt)
            with st.chat_message(name="assistant"):
                outer_dict["answer_area"] = st.empty()

    def post_process(self, outer_dict: Dict[str, Any], inner_dict: Dict[str, Any]) -> None:
        outer_dict["answer_area"].write(inner_dict["answer"])

    def callback_process(self, content: str, outer_dict: Dict[str, Any], inner_dict: Dict[str, Any]) -> None:
        outer_dict["answer_area"].write(content)


class ProcessersManager(BaseProcessersManager):
    def pre_process_for_starting(self, **kwargs) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        outer_dict = {}
        outer_dict["message_area"] = kwargs["message_area"]
        outer_dict["history_area"] = kwargs["history_area"]

        try:
            inner_dict = {}
            inner_dict["form_schema"] = FormSchema.from_entity(chat_gpt_model_entity=kwargs["chat_gpt_model_entity"], prompt=kwargs["prompt"])
        except:
            outer_dict["message_area"].warning("Please input form corectly.")
            raise EarlyStopProcessException()
        return outer_dict, inner_dict

    def pre_process_for_running(self, **kwargs) -> Dict[str, Any]:
        outer_dict = {}
        outer_dict["message_area"] = kwargs["message_area"]
        outer_dict["history_area"] = kwargs["history_area"]

        kwargs["message_area"].warning("RUNNING")
        return outer_dict

    def post_process(self, outer_dict: Dict[str, Any], inner_dict: Dict[str, Any]) -> None:
        outer_dict["message_area"].empty()
        st.balloons()
