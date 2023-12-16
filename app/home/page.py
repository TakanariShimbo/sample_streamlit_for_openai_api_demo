from textwrap import dedent

import streamlit as st

from .. import BasePage, WakeupComponent, WakeupSState, ChatGptComponent


class HomePage(BasePage):
    @classmethod
    def init(cls) -> None:
        WakeupSState.init()

    @classmethod
    def main(cls) -> None:
        if WakeupSState.get():
            WakeupComponent.display()
            st.rerun()

        ChatGptComponent.display()
