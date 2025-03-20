from adrcommon.utils import config
from adrcommon.utils.config import load_config
from adrcommon.secrets.provider import SecretProvider

ENDPOINTS = 'endpoints'
INFERENCE_YAML = 'inference.yaml'

def get_endpoint(secrets: SecretProvider, provider: str) -> [str, str]:
    api_key = secrets.get_api_key(provider)

    endpoint_data = config.get_app_config(load_config, INFERENCE_YAML)
    api_endpoint = endpoint_data[ENDPOINTS][provider]

    return api_endpoint, api_key
