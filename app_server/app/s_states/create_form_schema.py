from pydantic import BaseModel, Field

from model import AccountEntity


class CreateFormSchema(BaseModel):
    account_id: str
    title: str = Field(min_length=4)

    @classmethod
    def from_entity(cls, account_entity: AccountEntity, title: str) -> "CreateFormSchema":
        return cls(account_id=account_entity.account_id, title=title)