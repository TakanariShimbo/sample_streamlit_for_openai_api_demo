from time import sleep
from typing import Dict, Any

import streamlit as st

from .schema import FormSchema
from .. import BaseProcesser, BaseProcessersManager, EarlyStopProcessException
from model import DEFAULT_OPENAI_API_KEY
from handler import ChatGptHandler


class MainProcesser(BaseProcesser[str]):
    def main_process(self, **kwargs) -> Dict[str, Any]:
        client = ChatGptHandler.generate_client(api_key=DEFAULT_OPENAI_API_KEY)
        kwargs["answer"] = ChatGptHandler.query_streamly_answer_and_display(
            client=client,
            prompt=kwargs["form_schema"].prompt,
            model_type=kwargs["form_schema"].chat_gpt_model_type,
            callback_func=self.add_queue,
        )
        return kwargs

    def pre_process(self, **kwargs) -> None:
        with kwargs["history_area"]:
            with st.chat_message(name="user"):
                st.write(kwargs["form_schema"].prompt)
            with st.chat_message(name="assistant"):
                self.answer_area = st.empty()

    def post_process(self, **kwargs) -> None:
        self.answer_area.write(kwargs["answer"])

    def callback_process(self, content: str, **kwargs) -> None:
        self.answer_area.write(content)


class ProcessersManager(BaseProcessersManager):
    def pre_process_for_starting(self, **kwargs) -> Dict[str, Any]:
        with kwargs["form_area"]:
            kwargs["message_area"] = st.empty()

        try:
            kwargs["form_schema"] = FormSchema.from_entity(chat_gpt_model_entity=kwargs["chat_gpt_model_entity"], prompt=kwargs["prompt"])
        except:
            kwargs["message_area"].warning("Please input form corectly.")
            raise EarlyStopProcessException()

        return kwargs

    def pre_process_for_running(self, **kwargs) -> None:
        with kwargs["form_area"]:
            kwargs["message_area"] = st.empty()
        kwargs["message_area"].warning("RUNNING")

    def post_process(self, **kwargs) -> None:
        kwargs["message_area"].empty()
        st.balloons()
