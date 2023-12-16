from textwrap import dedent

import streamlit as st

from .s_states import ProcessersManagerSState
from .. import BaseComponent
from model import ChatGptModelTable


class ChatGptComponent(BaseComponent):
    @classmethod
    def init(cls) -> None:
        ProcessersManagerSState.init()

    @classmethod
    def main(cls) -> None:
        contents = dedent(
            """
            ### 🤖 OpenAI API Demo  
            """
        )
        st.markdown(contents)

        form_area = st.form(key="Form")
        with form_area:
            st.markdown("### Form")

            selected_model_entity = st.selectbox(
                label="Model Type",
                options=ChatGptModelTable.get_all_entities(),
                format_func=lambda enetity: enetity.label_en,
                key="ChatGptModelTypeSelectBox",
            )

            inputed_prompt = st.text_area(
                label="Prompt",
                key="ChatGptTextArea",
            )

            _, left_area, _, center_area, _, right_area, _ = st.columns([1, 3, 1, 3, 1, 3, 1])
            with left_area:
                is_run_pushed = st.form_submit_button(label="RUN", type="primary", use_container_width=True)
            with center_area:
                is_rerun_pushed = st.form_submit_button(label="RERUN", type="primary", use_container_width=True)
            with right_area:
                is_reset_pushed = st.form_submit_button(label="RESET", type="secondary", use_container_width=True)

        if is_run_pushed:
            ProcessersManagerSState.on_click_run(
                form_area=form_area,
                model_entity=selected_model_entity,
                prompt=inputed_prompt,
            )
        elif is_rerun_pushed:
            ProcessersManagerSState.on_click_rerun(
                form_area=form_area,
                model_entity=selected_model_entity,
                prompt=inputed_prompt,
            )
        elif is_reset_pushed:
            ProcessersManagerSState.on_click_reset()