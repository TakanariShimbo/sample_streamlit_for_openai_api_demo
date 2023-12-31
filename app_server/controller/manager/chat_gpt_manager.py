from typing import Callable, List

from ..handler import ChatGptHandler, convert_entity_to_message_param
from model import ChatMessageEntity, DEFAULT_OPENAI_API_KEY


class ChatGptManager:
    @staticmethod
    def query_streamly_answer_and_display(
        prompt: str,
        assistant_id: str,
        message_entities: List[ChatMessageEntity],
        callback_func: Callable[[str], None],
    ) -> str:
        client = ChatGptHandler.generate_client(api_key=DEFAULT_OPENAI_API_KEY)
        message_params = [convert_entity_to_message_param(role=message_entity.role_id, content=message_entity.content) for message_entity in message_entities]
        answer = ChatGptHandler.query_streamly_answer_and_display(
            client=client,
            prompt=prompt,
            assistant_id=assistant_id,
            message_prams=message_params,
            callback_func=callback_func,
        )
        return answer
