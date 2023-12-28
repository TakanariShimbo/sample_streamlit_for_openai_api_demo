from .enter_processers import EnterProcesser, EnterProcesserManager
from ..base import BaseSState


class EnterProcesserSState(BaseSState[EnterProcesserManager]):
    @staticmethod
    def get_name() -> str:
        return "ENTER_PROCESSER_MANAGER"

    @staticmethod
    def get_default() -> EnterProcesserManager:
        return EnterProcesserManager([EnterProcesser])

    @classmethod
    def on_click_run(cls, **kwargs) -> bool:
        processers_manager = cls.get()
        is_success = processers_manager.run_all(**kwargs)
        return is_success
