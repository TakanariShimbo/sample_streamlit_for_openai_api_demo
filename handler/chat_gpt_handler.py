from typing import Any, List, Callable

from openai import OpenAI


class ChatGptHandler:
    @staticmethod
    def query_answer(
        client: OpenAI,
        prompt: str,
        model_type: str,
        chat_history: List[Any] = [],
    ) -> str:
        copyed_chat_history = chat_history.copy()
        copyed_chat_history.append({"role": "user", "content": prompt})

        response = client.chat.completions.create(model=model_type, messages=copyed_chat_history)

        answer = response.choices[0].message.content
        if not answer:
            raise ValueError("Response from OpenAI API is empty.")
        return answer

    @staticmethod
    def query_answer_and_display_streamly(
        client: OpenAI,
        prompt: str,
        model_type: str,
        display_func: Callable[[str], None] = print,
        chat_history: List[Any] = [],
    ) -> str:
        copyed_chat_history = chat_history.copy()
        copyed_chat_history.append({"role": "user", "content": prompt})

        stream_response = client.chat.completions.create(
            model=model_type,
            messages=copyed_chat_history,
            stream=True,
        )

        answer = ""
        for chunk in stream_response:
            answer_peace = chunk.choices[0].delta.content or ""  # type: ignore
            answer += answer_peace
            display_func(answer)
        return answer