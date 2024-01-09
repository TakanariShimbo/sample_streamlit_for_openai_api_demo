from typing import Any, Optional, Type

from ..base import BaseEntity
from .config import AccountConfig


class AccountEntity(BaseEntity[AccountConfig]):
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
            raise ValueError("Not accessible due to have not constracted.")
        return registered_at.split(sep=" ")[0]

    def _check_is_same(self, other: Any) -> bool:
        return False

    @staticmethod
    def _get_config_class() -> Type[AccountConfig]:
        return AccountConfig