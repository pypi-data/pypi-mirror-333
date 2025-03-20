from __future__ import annotations

from enum import StrEnum
import typing as t
import json
import os
from pathlib import Path
import logging


import requests
from openai import OpenAI
import yaml
from protoai.typing import BaseURL, AIModels

logger = logging.getLogger('protoai')


def load_secret(path: Path = 'secret.yaml'):
    with open(path, 'r') as sec:
        config = yaml.safe_load(sec)
        if 'SECRET_KEY' not in config or 'USING' not in config:
            info = \
                "Secret file format error. Please config you secret file as below:\n"\
                "    ```\n"\
                "    SECRET_KEY:\n"\
                "        OPEN_AI: your_key\n"\
                "        OTHER_KEY: your_key\n"\
                "    USING: OPEN_AI\n"\
                "    ```\n"
            logger.error(info)
            raise KeyError(info)
        return config['SECRET_KEY'][config['USING']]


class ProtoAIConfig:

    base_url: BaseURL
    model: AIModels
    _secret: str

    def __init__(
        self,
        secret: Path = 'secret.yaml',
        model: AIModels = AIModels.GPT_4o,
        base_url: BaseURL = BaseURL.OPEN_AI
    ):
        super().__init__()
        self.model = model
        self._secret = load_secret(secret)
        self.base_url = base_url

    @property
    def api_chat(self):
        return self.base_url + "chat/completions"

    @property
    def headers(self):
        return {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {self._secret}'
        }


"""

default_payload = {}
default_headers = 


def chat(payload: Payload, full_result=False):
    response = requests.request(
        "POST",
        api_chat,
        headers={**default_headers, },
        data=payload.json
    )
    result = json.loads(response.text)
    if full_result:
        return json.loads(response.text)
    else:
        return result['choices'][0]['message']['content']


def models() -> list:
    client = OpenAI(api_key=apikey[ai_model],
                    base_url="https://api.deepseek.com")
    return client.models.list()


def request(
        api: str,
        headers: dict = default_headers,
        payload: dict = default_payload
) -> str:
    response = requests.request(
        "GET", api, headers=headers, data=payload)
    return response.text
"""
