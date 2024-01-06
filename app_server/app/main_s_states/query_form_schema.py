from typing import Optional

from pydantic import BaseModel, ValidationError, Field

from model import AssistantTypeEntity


class QueryFormSchema(BaseModel):
    assistant_id: str
    prompt: str = Field(min_length=1)

    @classmethod
    def from_entity(cls, assistant_entity: Optional[AssistantTypeEntity], prompt: str) -> "QueryFormSchema":
        if not assistant_entity:
            raise ValidationError("AssistantTypeEntity is None.")
        return cls(assistant_id=assistant_entity.assistant_id, prompt=prompt)