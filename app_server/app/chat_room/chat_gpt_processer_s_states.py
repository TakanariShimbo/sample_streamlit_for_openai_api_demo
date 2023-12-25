from .chat_gpt_processers import ChatGptProcesser, ChatGptProcesserManager
from ..base import BaseSState


class ChatGptProcesserSState(BaseSState[ChatGptProcesserManager]):
    @staticmethod
    def get_name() -> str:
        return "CHAT_GPT_PROCESSER_MANAGER"

    @staticmethod
    def get_default() -> ChatGptProcesserManager:
        return ChatGptProcesserManager([ChatGptProcesser])

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
