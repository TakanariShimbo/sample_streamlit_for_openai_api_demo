from typing import Dict, Any, Tuple

from .sign_in_form_schema import SignInFormSchema
from .account_s_states import AccountSState
from .main_component_s_states import MainComponentSState
from ..base import BaseProcesser, BaseProcessersManager, EarlyStopProcessException
from controller import AccountManager


class SignInProcesser(BaseProcesser[None]):
    def main_process(self, inner_dict: Dict[str, Any]) -> None:
        inner_dict["response"] = AccountManager.sign_in(
            account_id=inner_dict["form_schema"].account_id,
            raw_password=inner_dict["form_schema"].raw_password,
        )

    def pre_process(self, outer_dict: Dict[str, Any], inner_dict: Dict[str, Any]) -> None:
        pass

    def post_process(self, outer_dict: Dict[str, Any], inner_dict: Dict[str, Any]) -> None:
        pass

    def callback_process(self, content: None, outer_dict: Dict[str, Any], inner_dict: Dict[str, Any]) -> None:
        pass


class SignInProcesserManager(BaseProcessersManager):
    def pre_process_for_starting(self, **kwargs) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        outer_dict = {}
        outer_dict["message_area"] = kwargs["message_area"]

        try:
            inner_dict = {}
            inner_dict["form_schema"] = SignInFormSchema(account_id=kwargs["account_id"], raw_password=kwargs["raw_password"])
        except:
            outer_dict["message_area"].warning("Please input form corectly.")
            raise EarlyStopProcessException()
        return outer_dict, inner_dict

    def pre_process_for_running(self, **kwargs) -> Dict[str, Any]:
        outer_dict = {}
        outer_dict["message_area"] = kwargs["message_area"]

        kwargs["message_area"].warning("RUNNING")
        return outer_dict

    def post_process(self, outer_dict: Dict[str, Any], inner_dict: Dict[str, Any]) -> bool:
        if not inner_dict["response"].is_success:
            outer_dict["message_area"].warning(inner_dict["response"].message)
            return False

        AccountSState.set(value=inner_dict["response"].contents)
        MainComponentSState.set_home_entity()
        outer_dict["message_area"].empty()
        return True
