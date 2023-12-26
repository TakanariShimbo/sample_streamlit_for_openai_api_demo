from textwrap import dedent

import streamlit as st

from ..base import BaseComponent
from ..s_states import CreateProcesserSState


class HomeComponent(BaseComponent):
    @staticmethod
    def init() -> None:
        CreateProcesserSState.init()

    @staticmethod
    def main() -> None:
        """
        TITLE
        """
        content = dedent(
            f"""
            ### 🏠 Home
            
            #### About
            Welcome to demo site of ChatGPT 🧠  
            """
        )

        st.markdown(content)

        """
        Form
        """
        form_area = st.form(key="CreateForm")
        with form_area:
            st.markdown("#### Form")

            inputed_title = st.text_input(
                label="Title",
                placeholder="Input room title here.",
                key="RoomTitleTextInput",
            )

            message_area = st.empty()

            _, center_area, _ = st.columns([5, 3, 5])
            with center_area:
                is_create_pushed = st.form_submit_button(label="CREATE", type="primary", use_container_width=True)

        if is_create_pushed:
            with st.spinner("Creating room..."):
                is_success = CreateProcesserSState.on_click_run(
                    message_area=message_area,
                    title=inputed_title,
                )
            if is_success:
                st.rerun()

    @staticmethod
    def deinit() -> None:
        CreateProcesserSState.deinit()
