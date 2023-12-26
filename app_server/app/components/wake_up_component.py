from time import sleep

import streamlit as st
from streamlit_lottie import st_lottie

from ..base import BaseComponent
from ..main import ComponentSState
from controller import JsonHandler


class WakeupComponent(BaseComponent):
    WAKE_UP_LOGO = JsonHandler.load("./static/lotties/streamlit_logo.json")

    @classmethod
    def init(cls) -> None:
        pass

    @classmethod
    def main(cls) -> None:
        st_lottie(cls.WAKE_UP_LOGO, key="WakeUpLogo", speed=1.2, reverse=False, loop=False)
        sleep(4)
        ComponentSState.set_home_entity()
        st.rerun()

