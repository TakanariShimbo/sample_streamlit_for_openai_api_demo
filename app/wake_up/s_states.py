from .. import BaseSState


class WakeupSState(BaseSState[bool]):
    @staticmethod
    def get_name() -> str:
        return "WAKE_UP"

    @staticmethod
    def get_default() -> bool:
        return True

    @classmethod
    def compolete_wakeup(cls) -> None:
        cls.set(value=False)
