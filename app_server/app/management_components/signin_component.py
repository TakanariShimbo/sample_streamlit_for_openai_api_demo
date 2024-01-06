import streamlit as st

from .signin_action_results import ActionResults
from ..base import BaseComponent
from ..management_s_states import ManagementComponentSState
from model import ADMIN_ID, ADMIN_PASSWORD


class SignInComponent(BaseComponent):
    @staticmethod
    def init() -> None:
        pass

    @staticmethod
    def _display_title() -> None:
        st.markdown("### 👤 Sign in")

    @staticmethod
    def _display_sign_in_form_and_get_results() -> ActionResults:
        with st.form(key="SignInForm", border=True):
            inputed_admin_id = st.text_input(
                label="Admin ID",
                placeholder="Input admin id here.",
                key="AdminIdTextInput",
            )
            inputed_admin_password = st.text_input(
                label="Password",
                placeholder="Input password here.",
                key="PasswordTextInput",
                type="password",
            )
            message_area = st.empty()
            _, button_area, _ = st.columns([5, 3, 5])
            with button_area:
                is_pushed = st.form_submit_button(label="Enter", type="primary", use_container_width=True)

        return ActionResults(
            admin_id=inputed_admin_id,
            admin_password=inputed_admin_password,
            message_area=message_area,
            is_pushed=is_pushed,
        )

    @staticmethod
    def _execute_sign_in_process(action_results: ActionResults) -> bool:
        if not action_results.is_pushed:
            return False

        if not action_results.admin_id == ADMIN_ID:
            action_results.message_area.warning("Please input form corectly.")
            return False
        
        if not action_results.admin_password == ADMIN_PASSWORD:
            action_results.message_area.warning("Please input form corectly.")
            return False
        
        ManagementComponentSState.set_home_entity()
        return True

    @classmethod
    def main(cls) -> None:
        cls._display_title()
        action_results = cls._display_sign_in_form_and_get_results()
        is_success = cls._execute_sign_in_process(action_results=action_results)
        if is_success:
            cls.deinit()
            st.rerun()

    @staticmethod
    def deinit() -> None:
        pass
