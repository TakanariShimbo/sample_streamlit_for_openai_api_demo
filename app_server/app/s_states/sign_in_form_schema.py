from pydantic import BaseModel, Field


class SignInFormSchema(BaseModel):
    account_id: str = Field(min_length=4)
    raw_password: str = Field(min_length=4)

