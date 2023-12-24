from typing import Callable, List
from uuid import uuid4

from .. import ChatGptHandler, convert_entity_to_message_param
from model import ChatGptMessageEntity, ChatGptMessageTable, DEFAULT_OPENAI_API_KEY, DATABASE_ENGINE


class ChatGptMessagesManager:
    def __init__(self):
        self._table = ChatGptMessageTable.create_empty_table()
        self._room_id = str(uuid4())

    def add_prompt_and_answer(self, prompt: str, answer: str, user_id: str = "user", assistant_id: str = "assistant") -> None:
        prompt_and_answer_entitys = [
            ChatGptMessageEntity(room_id=self._room_id, role="user", sender_id=user_id, content=prompt),
            ChatGptMessageEntity(room_id=self._room_id, role="assistant", sender_id=assistant_id, content=answer),
        ]
        appended_table = ChatGptMessageTable.load_from_entities(entities=prompt_and_answer_entitys)
        appended_table.save_to_database(database_engine=DATABASE_ENGINE)
        self._table = ChatGptMessageTable.append_b_to_a(self._table, appended_table)

    def get_all_message_entities(self) -> List[ChatGptMessageEntity]:
        return self._table.get_all_entities()


class ChatGptQueryManager:
    @staticmethod
    def query_streamly_answer_and_display(
        prompt: str,
        model_type: str,
        message_entities: List[ChatGptMessageEntity],
        callback_func: Callable[[str], None],
    ) -> str:
        client = ChatGptHandler.generate_client(api_key=DEFAULT_OPENAI_API_KEY)
        message_params = [convert_entity_to_message_param(role=message_entity.role, content=message_entity.content) for message_entity in message_entities]
        answer = ChatGptHandler.query_streamly_answer_and_display(
            client=client,
            prompt=prompt,
            model_type=model_type,
            message_prams=message_params,
            callback_func=callback_func,
        )
        return answer
