import pytest
import json
from protoai.message import Message, Payload


def test_message_ask():
    msg = Message().append('观复博物馆在什么位置?').ask()
    assert 'choices' in msg.keys()
    assert len(msg['choices'][0]['message']['content']) > 0
    print(msg['choices'][0]['message']['content'])


def test_payload_data():
    payload = Payload()
    print(json.dumps(payload.data))
