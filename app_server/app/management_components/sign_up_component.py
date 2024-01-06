import streamlit as st
from streamlit_lottie import st_lottie_spinner

from .sign_up_action_results import ActionResults
from ..base import BaseComponent
from ..management_s_states import ManagementComponentSState, SignUpProcesserSState
from model import AccountTable, DATABASE_ENGINE
from controller import LottieManager


class SignUpComponent(BaseComponent):
    @staticmethod
    def init() -> None:
        SignUpProcesserSState.init()

    @classmethod
    def _display_sign_out_button(cls) -> None:
        st.sidebar.button(label="👤 Sign out", key="SignOutButton", on_click=cls._on_click_sign_out, use_container_width=True)

    @classmethod
    def _display_return_home_button(cls) -> None:
        st.sidebar.button(label="🏠 Home", key="ReturnHomeButton", on_click=cls._on_click_return_home, use_container_width=True)

    @staticmethod
    def _display_title() -> None:
        st.markdown("### ➕ Sign up")

    @staticmethod
    def _display_sign_up_form_and_get_results() -> ActionResults:
        with st.form(key="SignUpForm", border=True):
            inputed_account_id = st.text_input(
                label="Account ID",
                placeholder="Input account id here.",
                key="AccountIdTextInput",
            )
            inputed_raw_password = st.text_input(
                label="Password",
                placeholder="Input password here.",
                key="PasswordTextInput",
                type="password",
            )
            message_area = st.empty()
            _, button_area, _ = st.columns([5, 3, 5])
            with button_area:
                is_pushed = st.form_submit_button(label="Enter", type="primary", use_container_width=True)
            _, loading_area, _ = st.columns([1, 1, 1])

        return ActionResults(
            account_id=inputed_account_id,
            raw_password=inputed_raw_password,
            message_area=message_area,
            loading_area=loading_area,
            is_pushed=is_pushed,
        )

    @staticmethod
    def _execute_sign_up_process(action_results: ActionResults) -> None:
        if not action_results.is_pushed:
            return

        with action_results.loading_area:
            with st_lottie_spinner(animation_source=LottieManager.LOADING):
                processers_manager = SignUpProcesserSState.get()
                processers_manager.run_all(
                    message_area=action_results.message_area,
                    account_id=action_results.account_id,
                    raw_password=action_results.raw_password,
                )

    @staticmethod
    def _display_account_table() -> None:
        account_table = AccountTable.load_from_database(database_engine=DATABASE_ENGINE)
        st.dataframe(account_table.df, use_container_width=True)

    @classmethod
    def _on_click_sign_out(cls):
        ManagementComponentSState.set_sign_in_entity()
        cls.deinit()

    @classmethod
    def _on_click_return_home(cls):
        ManagementComponentSState.set_home_entity()
        cls.deinit()

    @classmethod
    def main(cls) -> None:
        cls._display_sign_out_button()
        cls._display_return_home_button()
        cls._display_title()
        action_results = cls._display_sign_up_form_and_get_results()
        cls._execute_sign_up_process(action_results=action_results)
        cls._display_account_table()

    @staticmethod
    def deinit() -> None:
        SignUpProcesserSState.deinit()