from .query_processers import QueryProcesser, QueryProcesserManager
from ..base import BaseSState


class QueryProcesserSState(BaseSState[QueryProcesserManager]):
    @staticmethod
    def get_name() -> str:
        return "QUERY_PROCESSER_MANAGER"

    @staticmethod
    def get_default() -> QueryProcesserManager:
        return QueryProcesserManager([QueryProcesser])

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
