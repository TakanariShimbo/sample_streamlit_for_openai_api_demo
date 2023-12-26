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
    def on_click_run(cls, **kwargs) -> bool:
        processer_manager = cls.get()
        is_success = processer_manager.run_all(**kwargs)
        return is_success
    
    @classmethod
    def on_click_cancel(cls) -> None:
        processer_manager = cls.get()
        processer_manager.init_processers()

    @classmethod
    def on_click_rerun(cls, **kwargs) -> bool:
        processer_manager = cls.get()
        processer_manager.init_processers()
        is_success = processer_manager.run_all(**kwargs)
        return is_success