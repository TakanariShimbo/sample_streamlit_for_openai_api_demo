from typing import Any, List, Optional

from ..base import BaseEntity


class AccountEntity(BaseEntity):
    def __init__(self, account_id: str, hashed_password: str, registered_at: Optional[str] = None) -> None:
        self._account_id = account_id
        self._hashed_password = hashed_password
        self._registered_at = registered_at

    @property
    def account_id(self) -> str:
        return self._account_id

    @property
    def hashed_password(self) -> str:
        return self._hashed_password

    @property
    def registered_at(self) -> str:
        registered_at = self._registered_at
        if registered_at == None:
            raise ValueError("Not accessible due to have not constracted yet.")
        return registered_at.split(sep=" ")[0]

    def check_is_same(self, other: Any) -> bool:
        return False

    @staticmethod
    def get_loading_columns() -> List[str]:
        return ["account_id", "hashed_password", "registered_at"]
    
    @staticmethod
    def get_saving_columns() -> List[str]:
        return ["account_id", "hashed_password"]
