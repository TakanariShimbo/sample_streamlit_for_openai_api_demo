from textwrap import dedent

import streamlit as st

from .. import BasePage, WakeupComponent, WakeupSState


class HomePage(BasePage):
    @classmethod
    def init(cls) -> None:
        WakeupSState.init()

    @classmethod
    def main(cls) -> None:
        if WakeupSState.get():
            WakeupComponent.display()
            st.rerun()

        st.markdown(
            dedent(
                """
                ### 🤖 OpenAI API Demo

                This is demo site of OpenAI API
                """
            )
        )
