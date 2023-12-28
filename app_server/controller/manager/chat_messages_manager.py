from typing import List
from uuid import uuid4

from model import ChatRoomEntity, ChatRoomTable, ChatMessageEntity, ChatMessageTable, DATABASE_ENGINE


class ChatMessagesManager:
    def __init__(self, chat_message_table: ChatMessageTable, room_id: str):
        self._table = chat_message_table
        self._room_id = room_id

    @classmethod
    def init_as_new(cls, title: str = "sample") -> "ChatMessagesManager":
        room_id = str(uuid4())
        chat_room_entity = ChatRoomEntity(room_id=room_id, title=title)
        room_table = ChatRoomTable.load_from_entities(entities=[chat_room_entity])
        room_table.save_to_database(database_engine=DATABASE_ENGINE)

        chat_message_table = ChatMessageTable.create_empty_table()
        return cls(chat_message_table=chat_message_table, room_id=room_id)

    @classmethod
    def init_as_continue(cls, room_id: str = "b414c711-8635-4d9e-9b15-90e5cbd835a1") -> "ChatMessagesManager":
        chat_message_table = ChatMessageTable.load_specified_room_from_database(database_engine=DATABASE_ENGINE, room_id=room_id)
        return cls(chat_message_table=chat_message_table, room_id=room_id)

    def add_prompt_and_answer(self, prompt: str, answer: str, user_id: str = "user", assistant_id: str = "assistant") -> None:
        prompt_and_answer_entitys = [
            ChatMessageEntity(room_id=self._room_id, role="user", account_id=user_id, content=prompt),
            ChatMessageEntity(room_id=self._room_id, role="assistant", account_id=assistant_id, content=answer),
        ]
        appended_table = ChatMessageTable.load_from_entities(entities=prompt_and_answer_entitys)
        appended_table.save_to_database(database_engine=DATABASE_ENGINE)
        self._table = ChatMessageTable.append_b_to_a(self._table, appended_table)

    def get_all_message_entities(self) -> List[ChatMessageEntity]:
        return self._table.get_all_entities()
