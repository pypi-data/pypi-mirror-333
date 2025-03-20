import logging
import json

from typing import List
from typing import Dict
from typing import Union
from typing import Optional
from typing import Tuple
from typing import Generator

from openai import OpenAI

from .base import ChatService
from .base import CHAT_RESPOSNE_CHUNK
from .template import OPENAI_SIMPLE_CHAT_TEMPLATE_ENGINE_TYPE
from .settings import OPENAI_SIMPLE_CHAT_LOGGER_NAME
from .settings import OPENAI_API_KEY
from .settings import OPENAI_BASE_URL
from .settings import OPENAI_CHAT_MODEL

__all__ = [
    "OpenAIChatService",
]
openai_simple_chat_logger = logging.getLogger(OPENAI_SIMPLE_CHAT_LOGGER_NAME)


class OpenAIChatService(ChatService):
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
        system_prompt: Optional[str] = "You are helpful assistance.",
        temperature: Optional[float] = 0.01,
        max_input_tokens: Optional[int] = None,
        max_output_tokens: Optional[int] = None,
        max_tokens: Optional[int] = None,
        template_engine: Optional[OPENAI_SIMPLE_CHAT_TEMPLATE_ENGINE_TYPE] = None,
        template_root: Optional[str] = None,
    ):
        super().__init__(
            temperature=temperature,
            max_input_tokens=max_input_tokens,
            max_output_tokens=max_output_tokens,
            max_tokens=max_tokens,
            template_engine=template_engine,
            template_root=template_root,
        )
        self.api_key = api_key or OPENAI_API_KEY
        self.base_url = base_url or OPENAI_BASE_URL
        self.model = model or OPENAI_CHAT_MODEL
        self.system_prompt = system_prompt
        self.llm = OpenAI(api_key=self.api_key, base_url=self.base_url)

    @classmethod
    def get_messages(
        cls,
        prompt: Union[str, List[Dict[str, str]]],
        histories: Optional[List[Tuple[str, str]]] = None,
        system_prompt: str = "You are helpful assistance.",
    ):
        """将文字版的prompt转化为messages数组。

        @parameter histories: 问答记录记录:
        ```
            histories = [
                ("question1", "answer1"),
                ("question2", "answer2"),
            ]
        ```
        """
        histories = histories or []
        history_messages = []
        for history in histories:
            history_messages.append({"role": "user", "content": history[0]})
            history_messages.append({"role": "assistant", "content": history[1]})

        if isinstance(prompt, str):
            result = [
                {"role": "system", "content": system_prompt},
            ]
            result += history_messages
            result += [
                {"role": "user", "content": prompt},
            ]
        else:
            result = prompt[:1] + history_messages + prompt[1:]
        return result

    def chat(
        self,
        prompt: Optional[str] = None,
        template: Optional[str] = None,
        histories: Optional[List[Tuple[str, str]]] = None,
        temperature: Optional[float] = None,
        max_input_tokens: Optional[int] = None,
        max_output_tokens: Optional[int] = None,
        max_tokens: Optional[int] = None,
        options: Optional[Dict] = None,
        **context,
    ) -> CHAT_RESPOSNE_CHUNK:
        options = options or {}
        temperature = temperature or self.temperature
        max_input_tokens = max_input_tokens or self.max_input_tokens
        max_output_tokens = max_output_tokens or self.max_output_tokens
        max_tokens = max_tokens or self.max_tokens
        final_prompt = self.get_final_prompt(
            prompt=prompt,
            template=template,
            **context,
        )
        messages = self.get_messages(
            prompt=final_prompt,
            histories=histories,
            system_prompt=self.system_prompt,
        )
        completions_parameters = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "stream": False,
        }
        if max_tokens:
            completions_parameters["max_tokens"] = max_tokens
        if max_output_tokens:
            completions_parameters["max_completion_tokens"] = max_output_tokens
        if options:
            completions_parameters.update(**options)
        try:

            result_info = self.llm.chat.completions.create(**completions_parameters)
            openai_simple_chat_logger.warning(
                json.dumps(
                    {
                        "base_url": self.base_url,
                        "request": completions_parameters,
                        "response": result_info.model_dump(),
                        "error": None,
                    },
                    ensure_ascii=False,
                )
            )
        except Exception as error:
            openai_simple_chat_logger.warning(
                json.dumps(
                    {
                        "base_url": self.base_url,
                        "request": completions_parameters,
                        "response": None,
                        "error": str(error),
                    },
                    ensure_ascii=False,
                )
            )
            raise error
        if (not result_info) or (not result_info.choices):
            raise RuntimeError(422, f"LLM service response failed: {result_info}")
        response = result_info.choices[0].message.content
        return response, result_info.model_dump()

    def streaming_chat(
        self,
        prompt: Optional[str] = None,
        template: Optional[str] = None,
        histories: Optional[List[Tuple[str, str]]] = None,
        temperature: Optional[float] = None,
        max_input_tokens: Optional[int] = None,
        max_output_tokens: Optional[int] = None,
        max_tokens: Optional[int] = None,
        options: Optional[Dict] = None,
        **context,
    ) -> Generator[CHAT_RESPOSNE_CHUNK, None, None]:
        options = options or {}
        temperature = temperature or self.temperature
        max_input_tokens = max_input_tokens or self.max_input_tokens
        max_output_tokens = max_output_tokens or self.max_output_tokens
        max_tokens = max_tokens or self.max_tokens
        final_prompt = self.get_final_prompt(
            prompt=prompt,
            template=template,
            **context,
        )
        messages = self.get_messages(
            prompt=final_prompt,
            histories=histories,
            system_prompt=self.system_prompt,
        )
        completions_parameters = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "stream": True,
            "stream_options": {"include_usage": True},
        }
        if max_tokens:
            completions_parameters["max_tokens"] = max_tokens
        if max_output_tokens:
            completions_parameters["max_completion_tokens"] = max_output_tokens
        if options:
            completions_parameters.update(**options)
        outputs = []
        try:
            for chunk in self.llm.chat.completions.create(**completions_parameters):
                outputs.append(chunk.model_dump())
                if (
                    chunk.choices
                    and chunk.choices[0].delta
                    and chunk.choices[0].delta.content
                ):
                    delta = chunk.choices[0].delta.content
                else:
                    delta = ""
                yield delta, chunk.model_dump()
            openai_simple_chat_logger.warning(
                json.dumps(
                    {
                        "base_url": self.base_url,
                        "request": completions_parameters,
                        "response": outputs,
                        "error": None,
                    },
                    ensure_ascii=False,
                )
            )
        except Exception as error:
            openai_simple_chat_logger.warning(
                json.dumps(
                    {
                        "base_url": self.base_url,
                        "request": completions_parameters,
                        "response": None,
                        "error": str(error),
                    },
                    ensure_ascii=False,
                )
            )
            raise error
