from pydantic import BaseModel, Field


class CreateFormSchema(BaseModel):
    title: str = Field(min_length=1)
