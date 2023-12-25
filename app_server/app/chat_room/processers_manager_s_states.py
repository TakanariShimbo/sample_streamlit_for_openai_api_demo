from .processers import MainProcesser, MainProcessersManager
from ..base import BaseSState


class ProcessersManagerSState(BaseSState[MainProcessersManager]):
    @staticmethod
    def get_name() -> str:
        return "MAIN_PROCESSERS_MANAGER"

    @staticmethod
    def get_default() -> MainProcessersManager:
        return MainProcessersManager([MainProcesser])

    @classmethod
    def on_click_run(cls, **kwargs) -> None:
        processers_manager = cls.get()
        processers_manager.run_all(**kwargs)

    @classmethod
    def on_click_cancel(cls) -> None:
        processers_manager = cls.get()
        processers_manager.init_processers()

    @classmethod
    def on_click_rerun(cls, **kwargs) -> None:
        processers_manager = cls.get()
        processers_manager.init_processers()
        processers_manager.run_all(**kwargs)
