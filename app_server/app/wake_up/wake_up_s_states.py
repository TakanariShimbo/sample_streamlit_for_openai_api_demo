from ..base import BaseSState


class WakeupSState(BaseSState[bool]):
    @staticmethod
    def get_name() -> str:
        return "IS_WAKING_UP"

    @staticmethod
    def get_default() -> bool:
        return True

    @classmethod
    def compolete_wakeup(cls) -> None:
        cls.set(value=False)
