from __future__ import annotations

import typing as t
from enum import StrEnum
import json
import requests

from .typing import MessageKey, MessageRole, AIModels
from .config.base import ProtoAIConfig


class Message:
    messages: t.List[t.Dict[MessageKey, t.Union[t.AnyStr, MessageRole]]]

    def __init__(self, msg: t.AnyStr = '你是一个讲中文的行车助理.', role: MessageRole = MessageRole.DEVELOPER):
        super().__init__()
        self.messages = [{
            MessageKey.CONTENT: msg,
            MessageKey.ROLE: role
        }]

    def append(self, msg: t.AnyStr, role: MessageRole = MessageRole.USER) -> Message:
        self.messages.append({
            MessageKey.CONTENT: msg,
            MessageKey.ROLE: role
        })

        return self

    def ask(self, payload: Payload = None, config: ProtoAIConfig = None) -> str:
        if not payload:
            payload = Payload()

        if not config:
            config = ProtoAIConfig()

        body = payload.data
        body.setdefault('messages', self.messages)
        print(json.dumps(body, ensure_ascii=False))

        response = requests.request(
            'POST',
            config.api_chat,
            headers=config.headers,
            data=json.dumps(body, ensure_ascii=False)
        )

        result = json.loads(response.text)
        if 'choices' not in result:
            raise RuntimeError(f"Fail response: {response.text}")

        return result['choices'][0]['message']['content']


class Payload:

    def __init__(
        self,
        model: AIModels = AIModels.GPT_4o_MINI,
        max_completion_tokens=4096,
        frequency_penalty=0,
        presence_penalty=0,
        response_format={
            "type": "text"
        },
        stop=None,
        stream=False,
        stream_options=None,
        temperature=1.3,
        top_p=1,
        tools=None,
        tool_choice=None,
        logprobs=False,
        top_logprobs=None
    ):
        super().__init__()
        self.model = model
        self.frequency_penalty = frequency_penalty
        self.max_completion_tokens = max_completion_tokens
        self.presence_penalty = presence_penalty
        self.response_format = response_format
        self.stop = stop
        self.stream = stream
        self.stream_options = stream_options
        self.temperature = temperature
        self.top_p = top_p
        self.tools = tools
        self.tool_choice = tool_choice
        self.logprobs = logprobs
        self.top_logprobs = top_logprobs

    @property
    def data(self):
        return {
            "model": self.model,
            "frequency_penalty": self.frequency_penalty,
            "max_completion_tokens": self.max_completion_tokens,
            "presence_penalty": self.presence_penalty,
            "response_format": self.response_format,
            "stop": self.stop,
            "stream": self.stream,
            "stream_options": self.stream_options,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "tools": self.tools,
            "tool_choice": self.tool_choice,
            "logprobs": self.logprobs,
            "top_logprobs": self.top_logprobs
        }
