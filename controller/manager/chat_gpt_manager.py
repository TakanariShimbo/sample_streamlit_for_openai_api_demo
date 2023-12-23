from typing import Callable, List, Iterator

from .. import ChatGptHandler, convert_entity_to_message_param
from model import ChatGptMessageEntity, ChatGptMessageTable, DEFAULT_OPENAI_API_KEY


class ChatGptMessagesManager:
    def __init__(self):
        self._table = ChatGptMessageTable.create_empty_table()

    def add_prompt_and_answer(self, prompt: str, answer: str, user_name: str = "user", assistant_name: str = "assistant") -> None:
        prompt_and_answer_entitys = [
            ChatGptMessageEntity(role="user", name=user_name, content=prompt),
            ChatGptMessageEntity(role="assistant", name=assistant_name, content=answer),
        ]

        appended_table = ChatGptMessageTable.load_from_entity_list(entity_list=prompt_and_answer_entitys)
        self._table = ChatGptMessageTable.append_b_to_a(self._table, appended_table)

    def get_all_message_entities(self) -> List[ChatGptMessageEntity]:
        return self._table.get_all_entities()

    def iterate_all_message_entities(self, include_system=False) -> Iterator[ChatGptMessageEntity]:
        for message_entity in self._table.get_all_entities():
            if not include_system and message_entity.role == "system":
                continue
            yield message_entity


class ChatGptQueryManager:
    @staticmethod
    def query_streamly_answer_and_display(
        prompt: str,
        model_type: str,
        message_entities: List[ChatGptMessageEntity],
        callback_func: Callable[[str], None],
    ) -> str:
        message_params = []
        for message_entity in message_entities:
            message_param = convert_entity_to_message_param(role=message_entity.role, content=message_entity.content)
            message_params.append(message_param)

        client = ChatGptHandler.generate_client(api_key=DEFAULT_OPENAI_API_KEY)

        answer = ChatGptHandler.query_streamly_answer_and_display(
            client=client,
            prompt=prompt,
            model_type=model_type,
            message_prams=message_params,
            callback_func=callback_func,
        )

        return answer