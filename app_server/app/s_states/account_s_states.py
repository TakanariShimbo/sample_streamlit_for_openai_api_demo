from ..base import BaseSState
from model import AccountEntity


class AccountSState(BaseSState[AccountEntity]):
    @staticmethod
    def get_name() -> str:
        return "SIGNED_IN_ACCOUNT"
