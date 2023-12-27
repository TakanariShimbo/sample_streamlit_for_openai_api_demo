from textwrap import dedent

import streamlit as st
from streamlit_lottie import st_lottie_spinner

from ..base import BaseComponent
from ..s_states import CreateProcesserSState
from controller import LottieManager


class HomeComponent(BaseComponent):
    @staticmethod
    def init() -> None:
        CreateProcesserSState.init()

    @classmethod
    def main(cls) -> None:
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

            _, button_area, _ = st.columns([5, 3, 5])
            with button_area:
                is_create_pushed = st.form_submit_button(label="CREATE", type="primary", use_container_width=True)

            _, loading_area, _ = st.columns([1, 1, 1])

        if is_create_pushed:
            with loading_area:
                with st_lottie_spinner(animation_source=LottieManager.LOADING):
                    is_success = CreateProcesserSState.on_click_run(
                        message_area=message_area,
                        title=inputed_title,
                    )
                if is_success:
                    cls.deinit()
                    st.rerun()

    @staticmethod
    def deinit() -> None:
        CreateProcesserSState.deinit()
