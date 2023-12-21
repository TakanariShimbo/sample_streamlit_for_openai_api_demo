from typing import Callable, List, Literal, Iterator, Optional, Tuple

from openai import OpenAI, Stream
from openai.types.chat import (
    ChatCompletionChunk,
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
    ChatCompletionAssistantMessageParam,
    ChatCompletionMessageParam,
)

from . import OpenAiHandler


class ChatMessage:
    def __init__(self, role: Literal["user", "assistant", "system"], name: str, content: str) -> None:
        self._role = role
        self._name = name
        self._content = content

    @property
    def role(self) -> str:
        return self._role

    @property
    def name(self) -> str:
        return self._name

    @property
    def content(self) -> str:
        return self._content

    def to_chat_completion_message_param(self) -> ChatCompletionMessageParam:
        if self._role == "user":
            return ChatCompletionUserMessageParam(role="user", content=self._content)
        elif self._role == "assistant":
            return ChatCompletionAssistantMessageParam(role="assistant", content=self._content)
        elif self._role == "system":
            return ChatCompletionSystemMessageParam(role="system", content=self._content)
        else:
            raise ValueError("user or assistant or system")


class ChatMessages:
    def __init__(self, chat_messages: Optional[List[ChatMessage]] = None) -> None:
        if chat_messages == None:
            chat_messages = []
        self._chat_messages = chat_messages

    def to_chat_completion_message_params(self) -> List[ChatCompletionMessageParam]:
        return [chat_message.to_chat_completion_message_param() for chat_message in self._chat_messages]

    def add_system_role(self, system_role: str) -> None:
        self._chat_messages.append(ChatMessage(role="system", name="system", content=system_role))

    def add_prompt(self, prompt: str, user_name: str = "user") -> None:
        self._chat_messages.append(ChatMessage(role="user", name=user_name, content=prompt))

    def add_answer(self, answer: str, assistant_name: str = "assistant") -> None:
        self._chat_messages.append(ChatMessage(role="assistant", name=assistant_name, content=answer))

    def add_prompt_and_answer(self, prompt: str, answer: str, user_name: str = "user", assistant_name: str = "assistant") -> None:
        self.add_prompt(prompt=prompt, user_name=user_name)
        self.add_answer(answer=answer, assistant_name=assistant_name)

    def duplicate(self) -> "ChatMessages":
        copied_chat_messages = self._chat_messages.copy()
        return ChatMessages(copied_chat_messages)

    def iterate(self, include_system=False) -> Iterator[ChatMessage]:
        for chat_message in self._chat_messages:
            if include_system and chat_message.role == "system":
                continue
            yield chat_message


class ChatGptHandler(OpenAiHandler):
    @classmethod
    def query_answer(
        cls,
        client: OpenAI,
        prompt: str,
        model_type: str = "gpt-3.5-turbo",
        chat_messages: Optional[List[ChatCompletionMessageParam]] = None,
    ) -> str:
        response = client.chat.completions.create(
            model=model_type,
            messages=cls.get_chat_messages_added_prompt(prompt=prompt, chat_messages=chat_messages),
        )

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
        chat_messages: Optional[List[ChatCompletionMessageParam]] = None,
        callback_func: Callable[[str], None] = print,
    ) -> str:
        streamly_answer = cls.query_streamly_answer(client=client, prompt=prompt, model_type=model_type, chat_messages=chat_messages)
        answer = cls.display_streamly_answer(streamly_answer=streamly_answer, callback_func=callback_func)
        return answer

    @classmethod
    def query_streamly_answer(
        cls,
        client: OpenAI,
        prompt: str,
        model_type: str = "gpt-3.5-turbo",
        chat_messages: Optional[List[ChatCompletionMessageParam]] = None,
    ) -> Stream[ChatCompletionChunk]:
        streamly_answer = client.chat.completions.create(
            model=model_type,
            messages=cls.get_chat_messages_added_prompt(prompt=prompt, chat_messages=chat_messages),
            stream=True,
        )

        return streamly_answer

    @staticmethod
    def display_streamly_answer(
        streamly_answer: Stream[ChatCompletionChunk],
        callback_func: Callable[[str], None] = print,
    ):
        answer = ""
        for chunk in streamly_answer:
            answer_peace = chunk.choices[0].delta.content or ""  # type: ignore
            answer += answer_peace
            callback_func(answer)
        return answer

    @staticmethod
    def get_chat_messages_added_prompt(prompt: str, chat_messages: Optional[List[ChatCompletionMessageParam]]) -> List[ChatCompletionMessageParam]:
        if chat_messages == None:
            chat_messages = []

        copyed_chat_messages = chat_messages.copy()
        copyed_chat_messages.append(ChatCompletionUserMessageParam(role="user", content=prompt))
        return copyed_chat_messages
