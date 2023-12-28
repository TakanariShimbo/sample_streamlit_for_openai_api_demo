import streamlit as st
from streamlit.delta_generator import DeltaGenerator
from streamlit_lottie import st_lottie_spinner

from ..base import BaseComponent
from ..s_states import SignInProcesserSState
from controller import LottieManager


class ActionResults:
    def __init__(
        self,
        account_id: str,
        raw_password: str,
        message_area: DeltaGenerator,
        loading_area: DeltaGenerator,
        is_pushed: bool,
    ) -> None:
        self._account_id = account_id
        self._raw_password = raw_password
        self._message_area = message_area
        self._loading_area = loading_area
        self._is_pushed = is_pushed

    @property
    def account_id(self):
        return self._account_id

    @property
    def raw_password(self):
        return self._raw_password

    @property
    def message_area(self):
        return self._message_area

    @property
    def loading_area(self):
        return self._loading_area

    @property
    def is_pushed(self):
        return self._is_pushed


class SignInComponent(BaseComponent):
    @staticmethod
    def init() -> None:
        SignInProcesserSState.init()

    @staticmethod
    def _display_title() -> None:
        st.markdown("### 👤 Sign in")

    @staticmethod
    def _display_sign_in_form_and_get_results() -> ActionResults:
        with st.form(key="SignInForm", border=True):
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
                is_pushed = st.form_submit_button(label="ENTER", type="primary", use_container_width=True)
            _, loading_area, _ = st.columns([1, 1, 1])

        return ActionResults(
            account_id=inputed_account_id,
            raw_password=inputed_raw_password,
            message_area=message_area,
            loading_area=loading_area,
            is_pushed=is_pushed,
        )

    @staticmethod
    def _execute_sign_in_process(action_results: ActionResults) -> bool:
        if not action_results.is_pushed:
            return False

        with action_results.loading_area:
            with st_lottie_spinner(animation_source=LottieManager.LOADING):
                processers_manager = SignInProcesserSState.get()
                is_success = processers_manager.run_all(
                    message_area=action_results.message_area,
                    account_id=action_results.account_id,
                    raw_password=action_results.raw_password,
                )
        return is_success

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
        SignInProcesserSState.deinit()
