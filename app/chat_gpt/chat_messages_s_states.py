import streamlit as st

from .. import BaseSState
from controller import ChatGptMessagesManager


class ChatMessagesSState(BaseSState[ChatGptMessagesManager]):
    @staticmethod
    def get_name() -> str:
        return "CHAT_GPT_MESSAGES_MANAGER"

    @staticmethod
    def get_default() -> ChatGptMessagesManager:
        return ChatGptMessagesManager()

    @classmethod
    def add_prompt_and_answer(cls, prompt: str, answer: str, user_name: str = "user", assistant_name: str = "assistant") -> None:
        manager = cls.get()
        manager.add_prompt_and_answer(prompt=prompt, answer=answer, user_name=user_name, assistant_name=assistant_name)

    @classmethod
    def display(cls) -> None:
        manager = cls.get()
        for message_entity in manager.get_all_message_entities():
            if message_entity.role == "system":
                continue
            with st.chat_message(name=message_entity.name):
                st.write(message_entity.content)