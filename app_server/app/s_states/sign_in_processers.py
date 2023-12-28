from typing import Dict, Any, Tuple

from .sign_in_form_schema import SignInFormSchema
from .component_s_states import ComponentSState
from ..base import BaseProcesser, BaseProcessersManager, EarlyStopProcessException
from controller import AccountManager


class SignInProcesser(BaseProcesser[None]):
    def main_process(self, inner_dict: Dict[str, Any]) -> None:
        inner_dict["is_success"] = AccountManager.sign_in(
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
        if not inner_dict["is_success"]:
            outer_dict["message_area"].warning("Please input form corectly.")
            return False
        outer_dict["message_area"].empty()
        ComponentSState.set_home_entity()
        return True