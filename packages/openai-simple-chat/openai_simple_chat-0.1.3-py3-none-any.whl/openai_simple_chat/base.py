from typing import Optional
from typing import List
from typing import Tuple
from typing import Dict
from typing import Generator
from typing import Union

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
    default_base_url = None
    default_api_key = None
    default_model = None
    default_temperature = None
    default_system_prompt = "You are helpful assistant."
    default_top_p = None

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_input_tokens: Optional[int] = None,
        max_output_tokens: Optional[int] = None,
        max_tokens: Optional[int] = None,
        template_engine: Optional[OPENAI_SIMPLE_CHAT_TEMPLATE_ENGINE_TYPE] = None,
        template_root: Optional[str] = None,
        top_p: Optional[float] = None,
        **kwargs,
    ):
        # 基本参数
        self.base_url = base_url or self.default_base_url
        self.api_key = api_key or self.default_api_key
        self.system_prompt = system_prompt or self.default_system_prompt
        # 对话时可重载的参数
        self.model = model or self.default_model
        self.temperature = temperature or self.default_temperature
        self.top_p = top_p or self.default_top_p
        self.max_input_tokens = max_input_tokens
        self.max_output_tokens = max_output_tokens
        self.max_tokens = max_tokens
        if (
            (self.max_tokens is None)
            and self.max_input_tokens
            and self.max_output_tokens
        ):
            self.max_tokens = self.max_input_tokens + max_output_tokens
        # 模板引擎相关参数
        self.template_engine = (
            template_engine or get_template_prompt_by_django_template_engine
        )
        self.template_root = template_root
        # 其它未定义参数
        self.kwargs = kwargs

    def get_final_prompt(
        self,
        prompt: Optional[str] = None,
        template: Optional[str] = None,
        **context,
    ):
        """利用模板引擎，生成最终的prompt提示词。"""
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

    def get_messages(
        self,
        prompt: Union[str, List[Dict[str, str]]],
        histories: Optional[List[Tuple[str, str]]] = None,
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
                {"role": "system", "content": self.system_prompt},
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
        messages: Optional[List[Dict[str, str]]] = None,
        prompt: Optional[str] = None,
        histories: Optional[List[Tuple[str, str]]] = None,
        template: Optional[str] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        max_input_tokens: Optional[int] = None,
        max_output_tokens: Optional[int] = None,
        max_tokens: Optional[int] = None,
        options: Optional[Dict] = None,
        **context,
    ) -> CHAT_RESPOSNE_CHUNK:
        """messages或prompt+histories二选一"""
        # 根据模板生成prompt最终版
        if prompt or template:
            prompt = self.get_final_prompt(
                prompt=prompt,
                template=template,
                **context,
            )
        # 生成最终的messages
        messages = messages or self.get_messages(
            prompt=prompt,
            histories=histories,
        )
        # 计算最终的可重载参数
        model = model or self.model
        temperature = temperature or self.temperature
        top_p = top_p or self.top_p
        max_input_tokens = max_input_tokens or self.max_input_tokens
        max_output_tokens = max_output_tokens or self.max_output_tokens
        max_tokens = max_tokens or self.max_tokens
        # 调用服务
        return self.do_chat(
            messages=messages,
            prompt=prompt,
            histories=histories,
            template=template,
            model=model,
            temperature=temperature,
            top_p=top_p,
            max_input_tokens=max_input_tokens,
            max_output_tokens=max_output_tokens,
            max_tokens=max_tokens,
            options=options,
            **context,
        )


    def streaming_chat(
        self,
        messages: Optional[List[Dict[str, str]]] = None,
        prompt: Optional[str] = None,
        histories: Optional[List[Tuple[str, str]]] = None,
        template: Optional[str] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        max_input_tokens: Optional[int] = None,
        max_output_tokens: Optional[int] = None,
        max_tokens: Optional[int] = None,
        options: Optional[Dict] = None,
        **context,
    ) -> Generator[CHAT_RESPOSNE_CHUNK, None, None]:
        """messages或prompt+histories二选一"""
        # 根据模板生成prompt最终版
        if prompt or template:
            prompt = self.get_final_prompt(
                prompt=prompt,
                template=template,
                **context,
            )
        # 生成最终的messages
        messages = messages or self.get_messages(
            prompt=prompt,
            histories=histories,
        )
        # 计算最终的可重载参数
        model = model or self.model
        temperature = temperature or self.temperature
        top_p = top_p or self.top_p
        max_input_tokens = max_input_tokens or self.max_input_tokens
        max_output_tokens = max_output_tokens or self.max_output_tokens
        max_tokens = max_tokens or self.max_tokens
        # 调用服务
        for chunk in self.do_streaming_chat(
            messages=messages,
            prompt=prompt,
            histories=histories,
            template=template,
            model=model,
            temperature=temperature,
            top_p=top_p,
            max_input_tokens=max_input_tokens,
            max_output_tokens=max_output_tokens,
            max_tokens=max_tokens,
            options=options,
            **context,
        ):
            yield chunk

    def do_chat(
        self,
        messages: Optional[List[Dict[str, str]]] = None,
        prompt: Optional[str] = None,
        histories: Optional[List[Tuple[str, str]]] = None,
        template: Optional[str] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        max_input_tokens: Optional[int] = None,
        max_output_tokens: Optional[int] = None,
        max_tokens: Optional[int] = None,
        options: Optional[Dict] = None,
        **context,
    ) -> CHAT_RESPOSNE_CHUNK:
        raise NotImplementedError()

    def do_streaming_chat(
        self,
        messages: Optional[List[Dict[str, str]]] = None,
        prompt: Optional[str] = None,
        histories: Optional[List[Tuple[str, str]]] = None,
        template: Optional[str] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        max_input_tokens: Optional[int] = None,
        max_output_tokens: Optional[int] = None,
        max_tokens: Optional[int] = None,
        options: Optional[Dict] = None,
        **context,
    ) -> Generator[CHAT_RESPOSNE_CHUNK, None, None]:
        raise NotImplementedError()

    def jsonchat(
        self,
        messages: Optional[List[Dict[str, str]]] = None,
        prompt: Optional[str] = None,
        histories: Optional[List[Tuple[str, str]]] = None,
        template: Optional[str] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        max_input_tokens: Optional[int] = None,
        max_output_tokens: Optional[int] = None,
        max_tokens: Optional[int] = None,
        options: Optional[Dict] = None,
        **context,
    ) -> Dict:
        response, response_info = self.chat(
            messages=messages,
            prompt=prompt,
            histories=histories,
            template=template,
            model=model,
            temperature=temperature,
            top_p=top_p,
            max_input_tokens=max_input_tokens,
            max_output_tokens=max_output_tokens,
            max_tokens=max_tokens,
            options=options,
            **context,
        )
        return parse_json_response(response), response_info
