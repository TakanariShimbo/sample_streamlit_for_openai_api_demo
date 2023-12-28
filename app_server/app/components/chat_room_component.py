from typing import Optional

import streamlit as st
from streamlit.delta_generator import DeltaGenerator

from ..base import BaseComponent
from ..s_states import QueryProcesserSState, ChatMessagesSState
from model import CHAT_GPT_MODEL_TYPE_TABLE, ChatGptModelTypeEntity


class ActionResults:
    def __init__(
        self,
        chat_gpt_model_entity: Optional[ChatGptModelTypeEntity],
        prompt: str,
        message_area: DeltaGenerator,
        is_run_pushed: bool,
        is_rerun_pushed: bool,
        is_cancel_pushed: bool,
    ) -> None:
        self._chat_gpt_model_entity = chat_gpt_model_entity
        self._prompt = prompt
        self._message_area = message_area
        self._is_run_pushed = is_run_pushed
        self._is_rerun_pushed = is_rerun_pushed
        self._is_cancel_pushed = is_cancel_pushed

    @property
    def chat_gpt_model_entity(self):
        return self._chat_gpt_model_entity

    @property
    def prompt(self):
        return self._prompt

    @property
    def message_area(self):
        return self._message_area

    @property
    def is_run_pushed(self):
        return self._is_run_pushed

    @property
    def is_rerun_pushed(self):
        return self._is_rerun_pushed

    @property
    def is_cancel_pushed(self):
        return self._is_cancel_pushed


class ChatRoomComponent(BaseComponent):
    @staticmethod
    def init() -> None:
        ChatMessagesSState.init()
        QueryProcesserSState.init()

    @staticmethod
    def _display_title() -> None:
        st.markdown("### 💬 ChatRoom")

    @staticmethod
    def _display_query_form_and_get_results() -> ActionResults:
        form_area = st.form(key="QueryForm")
        with form_area:
            st.markdown("#### Form")

            selected_chat_gpt_model_entity = st.selectbox(
                label="Model Type",
                options=CHAT_GPT_MODEL_TYPE_TABLE.get_all_entities(),
                format_func=lambda enetity: enetity.label_en,
                key="ChatGptModelTypeSelectBox",
            )

            inputed_prompt = st.text_area(
                label="Prompt",
                placeholder="Input prompt here.",
                key="PromptTextArea",
            )

            message_area = st.empty()

            _, left_area, _, center_area, _, right_area, _ = st.columns([1, 3, 1, 3, 1, 3, 1])
            with left_area:
                is_run_pushed = st.form_submit_button(label="RUN", type="primary", use_container_width=True)
            with center_area:
                is_rerun_pushed = st.form_submit_button(label="RERUN", type="primary", use_container_width=True)
            with right_area:
                is_cancel_pushed = st.form_submit_button(label="CANCEL", type="secondary", use_container_width=True)

        return ActionResults(
            chat_gpt_model_entity=selected_chat_gpt_model_entity,
            prompt=inputed_prompt,
            message_area=message_area,
            is_run_pushed=is_run_pushed,
            is_rerun_pushed=is_rerun_pushed,
            is_cancel_pushed=is_cancel_pushed,
        )

    @staticmethod
    def _display_history() -> DeltaGenerator:
        history_area = st.container(border=True)
        with history_area:
            st.markdown("#### History")
            ChatMessagesSState.display()
        return history_area

    @staticmethod
    def _execute_query_process(action_results: ActionResults, history_area: DeltaGenerator) -> None:
        if action_results.is_run_pushed:
            QueryProcesserSState.on_click_run(
                message_area=action_results.message_area,
                history_area=history_area,
                chat_gpt_model_entity=action_results.chat_gpt_model_entity,
                prompt=action_results.prompt,
            )
        elif action_results.is_rerun_pushed:
            QueryProcesserSState.on_click_rerun(
                message_area=action_results.message_area,
                history_area=history_area,
                chat_gpt_model_entity=action_results.chat_gpt_model_entity,
                prompt=action_results.prompt,
            )
        elif action_results.is_cancel_pushed:
            QueryProcesserSState.on_click_cancel()

    @classmethod
    def main(cls) -> None:
        cls._display_title()
        action_results = cls._display_query_form_and_get_results()
        history_area = cls._display_history()
        cls._execute_query_process(action_results=action_results, history_area=history_area)

    @staticmethod
    def deinit() -> None:
        ChatMessagesSState.deinit()
        QueryProcesserSState.deinit()
