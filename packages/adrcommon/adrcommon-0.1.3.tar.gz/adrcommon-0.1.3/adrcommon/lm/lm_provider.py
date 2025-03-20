from abc import ABC, abstractmethod
from typing import Type

from openai import Client, AsyncClient
from typing_extensions import TypeVar

from adrcommon.secrets.provider import SecretProvider
from .inference import get_endpoint

OPENAI = 'openai'


class LmAdapter(ABC):
    @abstractmethod
    async def __call__(self, *args, **kwargs): pass

LLM = TypeVar('LLM', bound=LmAdapter)


class LmProvider:
    def __init__(self, secrets: SecretProvider, adapter: Type[LLM]):
        self._secrets = secrets
        self._adapter = adapter

    def get_lm(self, model_name: str, provider: str = None, temperature=0.1, max_tokens=4000):
        provider = provider or OPENAI

        params = {
            'model': f'{OPENAI}/{model_name}',
            'temperature': temperature,
            'max_tokens': max_tokens,
        }

        if provider == OPENAI:
            return self._adapter(
                api_key=self._secrets.get_api_key(OPENAI),
                **params
            )
        else:
            api_endpoint, api_key = get_endpoint(self._secrets, provider)

            return self._adapter(
                api_key=api_key,
                api_base=api_endpoint,
                **params
            )

    def get_client(self):
        return Client(api_key=self._secrets.get_api_key(OPENAI), max_retries=10)

    def get_async_client(self):
        return AsyncClient(api_key=self._secrets.get_api_key(OPENAI), max_retries=10)
