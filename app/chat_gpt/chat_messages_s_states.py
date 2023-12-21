import streamlit as st

from .. import BaseSState
from handler import ChatMessages


class ChatMessagesSState(BaseSState[ChatMessages]):
    @staticmethod
    def get_name() -> str:
        return "CHAT_GPT_CHAT_MESSAGES"

    @staticmethod
    def get_default() -> ChatMessages:
        return ChatMessages()

    @classmethod
    def add_prompt_and_answer(cls, prompt: str, answer: str, user_name: str = "user", assistant_name: str = "assistant") -> None:
        chat_messages = cls.get()
        chat_messages.add_prompt_and_answer(prompt=prompt, answer=answer, user_name=user_name, assistant_name=assistant_name)

    @classmethod
    def display(cls) -> None:
        chat_messages = cls.get()
        for chat_message in chat_messages.iterate():
            with st.chat_message(name=chat_message.name):
                st.write(chat_message.content)