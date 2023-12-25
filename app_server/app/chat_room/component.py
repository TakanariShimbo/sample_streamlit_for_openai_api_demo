from textwrap import dedent

import streamlit as st

from .processers_manager_s_states import ChatGptProcesserSState
from .chat_messages_s_states import ChatRoomSState
from ..base import BaseComponent
from model import CHAT_GPT_MODEL_TYPE_TABLE


class ChatRoomComponent(BaseComponent):
    @classmethod
    def init(cls) -> None:
        ChatRoomSState.init()
        ChatGptProcesserSState.init()

    @classmethod
    def main(cls) -> None:
        """
        TITLE
        """
        st.markdown("### 💬 ChatRoom")

        """
        Form
        """
        form_area = st.form(key="Form")
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
                key="ChatGptTextArea",
            )

            message_area = st.empty()

            _, left_area, _, center_area, _, right_area, _ = st.columns([1, 3, 1, 3, 1, 3, 1])
            with left_area:
                is_run_pushed = st.form_submit_button(label="RUN", type="primary", use_container_width=True)
            with center_area:
                is_rerun_pushed = st.form_submit_button(label="RERUN", type="primary", use_container_width=True)
            with right_area:
                is_cancel_pushed = st.form_submit_button(label="CANCEL", type="secondary", use_container_width=True)

        """
        History
        """
        history_area = st.container(border=True)
        with history_area:
            st.markdown("#### History")
            ChatRoomSState.display()

        if is_run_pushed:
            ChatGptProcesserSState.on_click_run(
                message_area=message_area,
                history_area=history_area,
                chat_gpt_model_entity=selected_chat_gpt_model_entity,
                prompt=inputed_prompt,
            )
        elif is_rerun_pushed:
            ChatGptProcesserSState.on_click_rerun(
                message_area=message_area,
                history_area=history_area,
                chat_gpt_model_entity=selected_chat_gpt_model_entity,
                prompt=inputed_prompt,
            )
        elif is_cancel_pushed:
            ChatGptProcesserSState.on_click_cancel()
