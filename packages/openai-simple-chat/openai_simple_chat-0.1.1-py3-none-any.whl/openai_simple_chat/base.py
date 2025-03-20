from typing import Optional
from typing import List
from typing import Tuple
from typing import Dict
from typing import Generator

from .template import OPENAI_SIMPLE_CHAT_TEMPLATE_ENGINE_TYPE
from .template import get_template_prompt_by_django_template_engine
from .template import get_template_prompt
from .jsonutils import parse_json_response

__all__ = [
    "CHAT_RESPOSNE_CHUNK",
    "ChatService",
]

CHAT_RESPOSNE_CHUNK = Tuple[str, Dict]


class ChatService(object):
    def __init__(
        self,
        temperature: Optional[float] = 0.01,
        max_input_tokens: Optional[int] = None,
        max_output_tokens: Optional[int] = None,
        max_tokens: Optional[int] = None,
        template_engine: Optional[OPENAI_SIMPLE_CHAT_TEMPLATE_ENGINE_TYPE] = None,
        template_root: Optional[str] = None,
        **kwargs,
    ):
        self.temperature = temperature
        self.max_input_tokens = max_input_tokens
        self.max_output_tokens = max_output_tokens
        self.max_tokens = max_tokens
        if (
            (self.max_tokens is None)
            and self.max_input_tokens
            and self.max_output_tokens
        ):
            self.max_tokens = self.max_input_tokens + max_output_tokens
        self.template_engine = (
            template_engine or get_template_prompt_by_django_template_engine
        )
        self.template_root = template_root
        self.kwargs = kwargs

    def get_final_prompt(
        self,
        prompt: Optional[str] = None,
        template: Optional[str] = None,
        **context,
    ):
        if template:
            return get_template_prompt(
                template=template,
                prompt=prompt,
                template_engine=self.template_engine,
                template_root=self.template_root,
                **context,
            )
        else:
            return prompt

    def chat(
        self,
        prompt: Optional[str] = None,
        template: Optional[str] = None,
        histories: Optional[List[Tuple[str, str]]] = None,
        temperature: Optional[float] = None,
        max_input_tokens: Optional[int] = None,
        max_output_tokens: Optional[int] = None,
        options: Optional[Dict] = None,
        **context,
    ) -> CHAT_RESPOSNE_CHUNK:
        raise NotImplementedError()

    def streaming_chat(
        self,
        prompt: Optional[str] = None,
        template: Optional[str] = None,
        histories: Optional[List[Tuple[str, str]]] = None,
        temperature: Optional[float] = None,
        max_input_tokens: Optional[int] = None,
        max_output_tokens: Optional[int] = None,
        options: Optional[Dict] = None,
        **context,
    ) -> Generator[CHAT_RESPOSNE_CHUNK, None, None]:
        raise NotImplementedError()

    def jsonchat(
        self,
        prompt: Optional[str] = None,
        template: Optional[str] = None,
        histories: Optional[List[Tuple[str, str]]] = None,
        temperature: Optional[float] = None,
        max_input_tokens: Optional[int] = None,
        max_output_tokens: Optional[int] = None,
        options: Optional[Dict] = None,
        **context,
    ) -> Dict:
        response, response_info = self.chat(
            prompt=prompt,
            template=template,
            histories=histories,
            temperature=temperature,
            max_input_tokens=max_input_tokens,
            max_output_tokens=max_output_tokens,
            options=options,
            **context,
        )
        return parse_json_response(response), response_info
