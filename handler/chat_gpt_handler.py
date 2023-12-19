from typing import Any, List, Callable

from openai import OpenAI, Stream
from openai.types.chat import (
    ChatCompletionChunk,
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
    ChatCompletionAssistantMessageParam,
    ChatCompletionMessageParam,
)

from . import OpenAiHandler


class ChatGptHandler(OpenAiHandler):
    @classmethod
    def query_answer(
        cls,
        client: OpenAI,
        prompt: str,
        model_type: str = "gpt-3.5-turbo",
        chat_messages: List[ChatCompletionMessageParam] = [],
    ) -> str:
        copyed_chat_messages = chat_messages.copy()
        cls.add_prompt_to_messages(prompt=prompt, chat_messages=copyed_chat_messages)

        response = client.chat.completions.create(model=model_type, messages=copyed_chat_messages)

        answer = response.choices[0].message.content
        if not answer:
            raise ValueError("Response from OpenAI API is empty.")
        return answer

    @classmethod
    def query_streamly_answer_and_display(
        cls,
        client: OpenAI,
        prompt: str,
        model_type: str = "gpt-3.5-turbo",
        chat_history: List[ChatCompletionMessageParam] = [],
        callback_func: Callable[[str], None] = print,
    ) -> str:
        streamly_answer = cls.query_streamly_answer(client=client, prompt=prompt, model_type=model_type, chat_messages=chat_history)
        answer = cls.display_streamly_answer(streamly_answer=streamly_answer, callback_func=callback_func)
        return answer

    @classmethod
    def query_streamly_answer(
        cls,
        client: OpenAI,
        prompt: str,
        model_type: str = "gpt-3.5-turbo",
        chat_messages: List[ChatCompletionMessageParam] = [],
    ) -> Stream[ChatCompletionChunk]:
        copyed_chat_messages = chat_messages.copy()
        cls.add_prompt_to_messages(prompt=prompt, chat_messages=copyed_chat_messages)

        streamly_answer = client.chat.completions.create(
            model=model_type,
            messages=copyed_chat_messages,
            stream=True,
        )

        return streamly_answer

    @staticmethod
    def display_streamly_answer(
        streamly_answer: Stream[ChatCompletionChunk],
        callback_func: Callable[[str], None] = print,
        initital_answer="",
    ):
        answer = initital_answer
        for chunk in streamly_answer:
            answer_peace = chunk.choices[0].delta.content or ""  # type: ignore
            answer += answer_peace
            callback_func(answer)
        return answer

    @staticmethod
    def add_system_role_to_messages(
        system_role: str,
        chat_messages: List[ChatCompletionMessageParam],
    ) -> None:
        chat_messages.append(ChatCompletionSystemMessageParam(role="system", content=system_role))

    @staticmethod
    def add_prompt_to_messages(
        prompt: str,
        chat_messages: List[ChatCompletionMessageParam],
    ) -> None:
        chat_messages.append(ChatCompletionUserMessageParam(role="user", content=prompt))

    @staticmethod
    def add_answer_to_messages(
        answer: str,
        chat_messages: List[ChatCompletionMessageParam],
    ) -> None:
        chat_messages.append(ChatCompletionAssistantMessageParam(role="assistant", content=answer))
