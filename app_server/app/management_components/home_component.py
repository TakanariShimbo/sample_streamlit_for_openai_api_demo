from textwrap import dedent
from typing import Optional, Literal

import streamlit as st

from ..base import BaseComponent
from ..management_s_states import ManagementComponentSState


class HomeComponent(BaseComponent):
    @staticmethod
    def init() -> None:
        pass

    @classmethod
    def _display_sign_out_button(cls) -> None:
        st.sidebar.button(label="👤 Sign out", key="SignOutButton", on_click=cls._on_click_sign_out, use_container_width=True)

    @staticmethod
    def _display_title() -> None:
        st.markdown("### 🏠 Home")

    @classmethod
    def _on_click_sign_out(cls) -> None:
        ManagementComponentSState.set_sign_in_entity()
        cls.deinit()

    @classmethod
    def main(cls) -> None:
        cls._display_sign_out_button()
        cls._display_title()

    @staticmethod
    def deinit() -> None:
        pass
