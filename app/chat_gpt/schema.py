from typing import Optional

from pydantic import BaseModel, ValidationError, Field

from model import ChatGptModelEntity


class FormSchema(BaseModel):
    chat_gpt_model_type: str
    prompt: str = Field(min_length=1)

    @classmethod
    def from_entity(cls, chat_gpt_model_entity: Optional[ChatGptModelEntity], prompt: str) -> "FormSchema":
        if not chat_gpt_model_entity:
            raise ValidationError("ChatGptModelEntity is None.")
        return cls(chat_gpt_model_type=chat_gpt_model_entity.key, prompt=prompt)