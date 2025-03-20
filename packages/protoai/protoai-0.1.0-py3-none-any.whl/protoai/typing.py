from enum import StrEnum


class BaseURL(StrEnum):
    DEEPSEEK = 'https://api.deepseek.com/'
    OPEN_AI = 'https://api.openai.com/v1/'


class MessageRole(StrEnum):
    SYSTEM = 'system'
    DEVELOPER = 'developer'
    USER = 'user'
    ASSISTANT = 'assistant'
    TOOL = 'tool'


class MessageKey(StrEnum):
    CONTENT = 'content'
    ROLE = 'role'


class AIModels(StrEnum):
    GPT_4o = 'gpt-4o'
    GPT_4o_MINI = 'gpt-4o-mini'
    GPT_4_5_PREVIEW = 'gpt-4.5-preview'
