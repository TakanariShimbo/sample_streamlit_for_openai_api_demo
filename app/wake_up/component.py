from time import sleep

import streamlit as st
from streamlit_lottie import st_lottie

from .s_states import WakeupSState
from .. import BaseComponent
from handler.json_handler import JsonHandler


class WakeupComponent(BaseComponent):
    WAKE_UP_LOGO = JsonHandler.load("./static/lotties/uniontool_logo.json")

    @classmethod
    def init(cls) -> None:
        WakeupSState.init()

    @classmethod
    def main(cls) -> None:
        st_lottie(cls.WAKE_UP_LOGO, key="WAKE_UP_LOGO", speed=1.2, reverse=False, loop=False)
        sleep(4)
        WakeupSState.compolete_wakeup()

    @classmethod
    def display_and_rerun_only_first_time(cls):
        cls.init()
        if WakeupSState.get():
            cls.display()
            st.rerun()
