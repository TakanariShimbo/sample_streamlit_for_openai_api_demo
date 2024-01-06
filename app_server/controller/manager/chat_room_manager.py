from typing import List
from uuid import uuid4

from model import ChatRoomEntity, ChatRoomTable, ChatMessageEntity, ChatMessageTable, ROLE_TYPE_TABLE, DATABASE_ENGINE


class ChatRoomManager:
    def __init__(self, chat_message_table: ChatMessageTable, room_id: str, account_id: str, release_id: str):
        self._table = chat_message_table
        self._room_id = room_id
        self._release_id = release_id
        self._account_id = account_id

    @property
    def account_id(self) -> str:
        return self._account_id

    @property
    def release_id(self) -> str:
        return self._release_id

    @classmethod
    def init_as_new(cls, title: str, account_id: str, release_id: str) -> "ChatRoomManager":
        room_id = str(uuid4())
        chat_room_entity = ChatRoomEntity(room_id=room_id, account_id=account_id, title=title, release=release_id)
        chat_room_table = ChatRoomTable.load_from_entities(entities=[chat_room_entity])
        chat_room_table.save_to_database(database_engine=DATABASE_ENGINE)

        chat_message_table = ChatMessageTable.create_empty_table()
        return cls(chat_message_table=chat_message_table, room_id=room_id, account_id=account_id, release_id=release_id)

    @classmethod
    def init_as_continue(cls, room_id: str, account_id: str, release_id: str) -> "ChatRoomManager":
        chat_message_table = ChatMessageTable.load_messages_specified_room_from_database(database_engine=DATABASE_ENGINE, room_id=room_id)
        return cls(chat_message_table=chat_message_table, room_id=room_id, account_id=account_id, release_id=release_id)

    def add_prompt_and_answer(self, prompt: str, answer: str, account_id: str, assistant_id: str) -> None:
        prompt_and_answer_entitys = [
            ChatMessageEntity(room_id=self._room_id, role=ROLE_TYPE_TABLE.get_user_entity().role_id, sender_id=account_id, content=prompt),
            ChatMessageEntity(room_id=self._room_id, role=ROLE_TYPE_TABLE.get_assistant_entity().role_id, sender_id=assistant_id, content=answer),
        ]
        appended_table = ChatMessageTable.load_from_entities(entities=prompt_and_answer_entitys)
        appended_table.save_to_database(database_engine=DATABASE_ENGINE)
        self._table = ChatMessageTable.append_b_to_a(self._table, appended_table)

    def get_all_message_entities(self) -> List[ChatMessageEntity]:
        return self._table.get_all_entities()
