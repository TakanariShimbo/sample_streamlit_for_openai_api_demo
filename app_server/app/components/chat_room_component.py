from typing import Optional

import streamlit as st
from streamlit.delta_generator import DeltaGenerator

from ..base import BaseComponent
from ..s_states import AccountSState, ComponentSState, QueryProcesserSState, ChatMessagesSState
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
    def chat_gpt_model_entity(self) -> Optional[ChatGptModelTypeEntity]:
        return self._chat_gpt_model_entity

    @property
    def prompt(self) -> str:
        return self._prompt

    @property
    def message_area(self) -> DeltaGenerator:
        return self._message_area

    @property
    def is_run_pushed(self) -> bool:
        return self._is_run_pushed

    @property
    def is_rerun_pushed(self) -> bool:
        return self._is_rerun_pushed

    @property
    def is_cancel_pushed(self) -> bool:
        return self._is_cancel_pushed


class ChatRoomComponent(BaseComponent):
    @staticmethod
    def init() -> None:
        AccountSState.init()
        ChatMessagesSState.init()
        QueryProcesserSState.init()

    @classmethod
    def _display_sing_out_button(cls) -> None:
        st.sidebar.button(label="👤 Sign out", key="SignOutButton", on_click=cls._on_click_sign_out, use_container_width=True)

    @classmethod
    def _display_leave_room_button(cls) -> None:
        st.sidebar.button(label="🚪 Leave room", key="LeaveRoomButton", on_click=cls._on_click_leave_room, use_container_width=True)

    @staticmethod
    def _display_title() -> None:
        st.markdown("### 💬 Chat Room")

    @staticmethod
    def _display_query_form_and_get_results() -> ActionResults:
        st.markdown("#### 🧠 Query")
        form_area = st.form(key="QueryForm")
        with form_area:
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
        history_area = st.container(border=False)
        with history_area:
            st.markdown("#### 📝 History")
            chat_messages_manager = ChatMessagesSState.get()
            for message_entity in chat_messages_manager.get_all_message_entities():
                if message_entity.role == "system":
                    continue
                with st.chat_message(name=message_entity.role):
                    st.write(message_entity.content)
        return history_area

    @staticmethod
    def _execute_query_process(action_results: ActionResults, history_area: DeltaGenerator) -> None:
        processer_manager = QueryProcesserSState.get()
        if action_results.is_rerun_pushed or action_results.is_cancel_pushed:
            processer_manager.init_processers()

        if action_results.is_run_pushed or action_results.is_rerun_pushed:
            processer_manager.run_all(
                message_area=action_results.message_area,
                history_area=history_area,
                chat_gpt_model_entity=action_results.chat_gpt_model_entity,
                prompt=action_results.prompt,
            )

    @classmethod
    def _on_click_sign_out(cls):
        ComponentSState.set_sign_in_entity()
        cls.deinit()
        AccountSState.deinit()

    @classmethod
    def _on_click_leave_room(cls):
        ComponentSState.set_home_entity()
        cls.deinit()

    @classmethod
    def main(cls) -> None:
        cls._display_sing_out_button()
        cls._display_leave_room_button()
        cls._display_title()
        action_results = cls._display_query_form_and_get_results()
        history_area = cls._display_history()
        cls._execute_query_process(action_results=action_results, history_area=history_area)

    @staticmethod
    def deinit() -> None:
        ChatMessagesSState.deinit()
        QueryProcesserSState.deinit()
