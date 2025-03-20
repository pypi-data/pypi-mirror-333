from abc import ABC, abstractmethod
from typing import Dict

import yaml
from pathlib import Path

from adrcommon.utils import util
from adrcommon.constants import CONF

SECRETS_DIR = '.secrets'
SECRETS = 'secrets'
API_KEYS = 'api-keys'


class SecretProvider(ABC):
    def get_api_key(self, name: str) -> str | Dict[str, str]:
        return self.get(API_KEYS).get(name)
    
    @abstractmethod
    def get(self, name: str) -> str | Dict[str, str]: pass


class ProjectSecrets(SecretProvider):
    def get(self, name: str) -> str | Dict[str, str]:
        data = Path(util.get_resources_dir(), CONF, '.'.join([SECRETS, 'yaml'])).read_text()
        data = yaml.safe_load(data)
        
        return data[name]


class UserSecrets(SecretProvider):
    def __init__(self, name = None):
        self._name = name or SECRETS

    def get(self, name: str) -> str | Dict[str, str]:
        data = Path(Path.home(), SECRETS_DIR, '.'.join([self._name, 'yaml'])).read_text()
        data = yaml.safe_load(data)

        return data[name]
