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
    def add_prompt_and_answer(cls, prompt: str, answer: str) -> None:
        chat_messages = cls.get()
        chat_messages.add_prompt_and_answer(prompt=prompt, answer=answer)

    @classmethod
    def display(cls) -> None:
        chat_messages = cls.get()
        for message_type, content in chat_messages.iterate():
            with st.chat_message(name=message_type):
                st.write(content)