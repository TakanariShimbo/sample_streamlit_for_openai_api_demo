from time import sleep

import streamlit as st
from streamlit_lottie import st_lottie

from ..base import BaseComponent
from ..s_states import ComponentSState
from controller import LottieManager


class WakeupComponent(BaseComponent):
    @staticmethod
    def init() -> None:
        pass

    @classmethod
    def main(cls) -> None:
        st_lottie(animation_source=LottieManager.WAKE_UP_LOGO, speed=1.2, reverse=False, loop=False)
        sleep(4)
        ComponentSState.set_sign_in_entity()
        st.rerun()

    @staticmethod
    def deinit() -> None:
        pass
