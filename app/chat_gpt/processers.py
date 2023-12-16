from time import sleep
from typing import Dict, Any

import streamlit as st

from .schema import FormSchema
from .. import BaseProcesser, BaseProcessersManager, EarlyStopProcessException
from model import DEFAULT_OPENAI_API_KEY
from handler import ChatGptHandler


class MainProcesser(BaseProcesser):
    def main_process(self, **kwargs) -> Dict[str, Any]:
        client = ChatGptHandler.generate_client(api_key=DEFAULT_OPENAI_API_KEY)
        kwargs["streamly_answer"] = ChatGptHandler.query_streamly_answer(
            client=client, 
            prompt=kwargs["form_schema"].prompt, 
            model_type=kwargs["form_schema"].model_type,
        )
        return kwargs

    def pre_process(self, **kwargs) -> None:
        st.markdown("#### History")
        with st.chat_message(name="user"):
            st.write(kwargs["form_schema"].prompt)

    def post_process(self, **kwargs) -> None:
        with st.chat_message(name="assistant"):
            answer_area = st.empty()
        ChatGptHandler.display_streamly_answer(streamly_answer=kwargs["streamly_answer"], display_func=answer_area.write)


class ProcessersManager(BaseProcessersManager):
    def pre_process_for_starting(self, **kwargs) -> Dict[str, Any]:
        with kwargs["form_area"]:
            kwargs["message_area"] = st.empty()

        try:
            kwargs["form_schema"] = FormSchema.from_entity(model_entity=kwargs["model_entity"], prompt=kwargs["prompt"])
        except:
            kwargs["message_area"].warning("Please input form corectly.")
            raise EarlyStopProcessException()

        kwargs["message_area"].info("START")
        return kwargs

    def pre_process_for_running(self, **kwargs) -> None:
        with kwargs["form_area"]:
            kwargs["message_area"] = st.empty()
        kwargs["message_area"].warning("RUNNING")

    def post_process(self, **kwargs) -> None:
        kwargs["message_area"].empty()
        st.balloons()