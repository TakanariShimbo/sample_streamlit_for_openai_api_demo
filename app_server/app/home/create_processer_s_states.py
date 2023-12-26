from typing import Optional

from .create_processers import CreateProcesser, CreateProcesserManager
from ..base import BaseSState
from controller import ChatMessagesManager


class CreateProcesserSState(BaseSState[CreateProcesserManager]):
    @staticmethod
    def get_name() -> str:
        return "CREATE_PROCESSER_MANAGER"

    @staticmethod
    def get_default() -> CreateProcesserManager:
        return CreateProcesserManager([CreateProcesser])

    @classmethod
    def on_click_run(cls, **kwargs) -> Optional[ChatMessagesManager]:
        processers_manager = cls.get()
        processers_manager.run_all(**kwargs)
        if not "manager" in processers_manager.inner_dict:
            return None
        return processers_manager.inner_dict["manager"]
