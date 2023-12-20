from .processers import MainProcesser, ProcessersManager
from .. import BaseSState


class ProcessersManagerSState(BaseSState[ProcessersManager]):
    @staticmethod
    def get_name() -> str:
        return "CHAT_GPT_PROCESSERS_MANAGER"

    @staticmethod
    def get_default() -> ProcessersManager:
        return ProcessersManager([MainProcesser])

    @classmethod
    def on_click_run(cls, **kwargs) -> None:
        processers_manager = cls.get()
        processers_manager.run_all(**kwargs)

    @classmethod
    def on_click_reset(cls) -> None:
        processers_manager = cls.get()
        processers_manager.init_processers()

    @classmethod
    def on_click_rerun(cls, **kwargs) -> None:
        processers_manager = cls.get()
        processers_manager.init_processers()
        processers_manager.run_all(**kwargs)