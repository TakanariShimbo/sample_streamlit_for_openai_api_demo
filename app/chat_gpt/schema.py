from typing import Optional

from pydantic import BaseModel, ValidationError, Field

from model import ChatGptModelEntity


class FormSchema(BaseModel):
    model_type: str
    prompt: str = Field(min_length=1)

    @classmethod
    def from_entity(cls, model_entity: Optional[ChatGptModelEntity], prompt: str) -> "FormSchema":
        if not model_entity:
            raise ValidationError("ChatGptEntity is None.")
        return cls(model_type=model_entity.key, prompt=prompt)