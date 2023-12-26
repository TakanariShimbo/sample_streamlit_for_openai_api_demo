from time import sleep

import streamlit as st
from streamlit_lottie import st_lottie

from ..base import BaseComponent
from ..s_states import ComponentSState
from controller import JsonHandler


WAKE_UP_LOGO = JsonHandler.load("./static/lotties/streamlit_logo.json")


class WakeupComponent(BaseComponent):
    @staticmethod
    def init() -> None:
        pass

    @staticmethod
    def main() -> None:
        st_lottie(WAKE_UP_LOGO, key="WakeUpLogo", speed=1.2, reverse=False, loop=False)
        sleep(4)
        ComponentSState.set_home_entity()
        st.rerun()

    @staticmethod
    def deinit() -> None:
        pass
