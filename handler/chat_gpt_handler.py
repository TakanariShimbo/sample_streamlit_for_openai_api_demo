from typing import Callable, List, Iterator, Tuple

from openai import OpenAI, Stream
from openai.types.chat import (
    ChatCompletionChunk,
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
    ChatCompletionAssistantMessageParam,
    ChatCompletionMessageParam,
)

from . import OpenAiHandler


class ChatMessages:
    def __init__(self, chat_messages: List[ChatCompletionMessageParam] = []) -> None:
        self._chat_messages = chat_messages

    @property
    def value(self) -> List[ChatCompletionMessageParam]:
        return self._chat_messages

    def add_system_role(self, system_role: str) -> None:
        self._chat_messages.append(ChatCompletionSystemMessageParam(role="system", content=system_role))

    def add_prompt(self, prompt: str) -> None:
        self._chat_messages.append(ChatCompletionUserMessageParam(role="user", content=prompt))

    def add_answer(self, answer: str) -> None:
        self._chat_messages.append(ChatCompletionAssistantMessageParam(role="assistant", content=answer))

    def add_prompt_and_answer(self, prompt: str, answer: str) -> None:
        self.add_prompt(prompt=prompt)
        self.add_answer(answer=answer)

    def duplicate(self) -> "ChatMessages":
        copied_chat_messages = self._chat_messages.copy()
        return ChatMessages(copied_chat_messages)
    
    def iterate(self) -> Iterator[Tuple[str, str]]:
        for chat_message in self._chat_messages:
            if chat_message["role"] == "system":
                continue
            yield chat_message["role"], chat_message["content"]  # type: ignore


class ChatGptHandler(OpenAiHandler):
    @classmethod
    def query_answer(
        cls,
        client: OpenAI,
        prompt: str,
        model_type: str = "gpt-3.5-turbo",
        chat_messages: ChatMessages = ChatMessages(),
    ) -> str:
        copyed_chat_messages = chat_messages.duplicate()
        copyed_chat_messages.add_prompt(prompt=prompt)

        response = client.chat.completions.create(model=model_type, messages=copyed_chat_messages.value)

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
        chat_messages: ChatMessages = ChatMessages(),
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
        chat_messages: ChatMessages = ChatMessages(),
    ) -> Stream[ChatCompletionChunk]:
        copyed_chat_messages = chat_messages.duplicate()
        copyed_chat_messages.add_prompt(prompt=prompt)

        streamly_answer = client.chat.completions.create(
            model=model_type,
            messages=copyed_chat_messages.value,
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
