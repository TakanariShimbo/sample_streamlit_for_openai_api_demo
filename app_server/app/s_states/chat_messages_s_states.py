import streamlit as st

from ..base import BaseSState
from controller import ChatMessagesManager


class ChatMessagesSState(BaseSState[ChatMessagesManager]):
    @staticmethod
    def get_name() -> str:
        return "CHAT_MESSAGES_MANAGER"

    @classmethod
    def add_prompt_and_answer(cls, prompt: str, answer: str, user_id: str = "sample_user", assistant_id: str = "assistant") -> None:
        chat_messages_manager = cls.get()
        chat_messages_manager.add_prompt_and_answer(prompt=prompt, answer=answer, user_id=user_id, assistant_id=assistant_id)

    @classmethod
    def display(cls) -> None:
        chat_messages_manager = cls.get()
        for message_entity in chat_messages_manager.get_all_message_entities():
            if message_entity.role == "system":
                continue
            with st.chat_message(name=message_entity.account_id):
                st.write(message_entity.content)