from typing import Any, List, Callable

from openai import OpenAI, Stream
from openai.types.chat import ChatCompletionChunk, ChatCompletionUserMessageParam

from . import OpenAiHandler


class ChatGptHandler(OpenAiHandler):
    @staticmethod
    def query_answer(
        client: OpenAI,
        prompt: str,
        model_type: str,
        chat_history: List[Any] = [],
    ) -> str:
        copyed_chat_history = chat_history.copy()
        copyed_chat_history.append(ChatCompletionUserMessageParam(role="user", content=prompt))

        response = client.chat.completions.create(model=model_type, messages=copyed_chat_history)

        answer = response.choices[0].message.content
        if not answer:
            raise ValueError("Response from OpenAI API is empty.")
        return answer

    @classmethod
    def query_streamly_answer_and_display(
        cls,
        client: OpenAI,
        prompt: str,
        model_type: str,
        chat_history: List[Any] = [],
        display_func: Callable[[str], None] = print,
    ) -> str:
        streamly_answer = cls.query_streamly_answer(client=client, prompt=prompt, model_type=model_type, chat_history=chat_history)
        answer = cls.display_streamly_answer(streamly_answer=streamly_answer, display_func=display_func)
        return answer
    
    @staticmethod
    def query_streamly_answer(
        client: OpenAI,
        prompt: str,
        model_type: str,
        chat_history: List[Any] = [],
    ) -> Stream[ChatCompletionChunk]:
        copyed_chat_history = chat_history.copy()
        copyed_chat_history.append(ChatCompletionUserMessageParam(role="user", content=prompt))

        streamly_answer = client.chat.completions.create(
            model=model_type,
            messages=copyed_chat_history,
            stream=True,
        )

        return streamly_answer

    @staticmethod
    def display_streamly_answer(
        streamly_answer: Stream[ChatCompletionChunk],
        display_func: Callable[[str], None] = print,
    ):
        answer = ""
        for chunk in streamly_answer:
            answer_peace = chunk.choices[0].delta.content or ""  # type: ignore
            answer += answer_peace
            display_func(answer)
        return answer