from pathlib import Path
from typing import Dict, Any, MutableMapping

import yaml
from mergedeep import merge

from adrcommon import constants
from .util import get_resources_dir, get_work_dir


def load_config(path: Path) -> Dict[str, Any]:
    if path.exists(follow_symlinks=True):
        return yaml.safe_load(path.read_text())
    return {}


def get_dynamic_config(config_name: str) -> Path:
    return Path(get_work_dir(constants.CONF), config_name)

def get_static_config(config_name: str) -> Path:
    return Path(get_resources_dir(), constants.CONF, config_name)

def get_app_config(parser, config_name: str) -> MutableMapping[str, Any]:
    static_config = get_static_config(config_name)
    dynamic_config = get_dynamic_config(config_name)

    app_config = merge({}, parser(static_config), parser(dynamic_config))
    return app_config
