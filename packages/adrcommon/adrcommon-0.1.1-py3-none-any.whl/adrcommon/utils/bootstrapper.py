import inspect
import logging
from pathlib import Path
from typing import Any



from adrcommon.constants import ROOT_DIR, APP_LOG
from . import util
from .cglobals import cglobals


class Bootstrapper:
    def __init__(self, root: Any = None):
        self._root = root or self

    def _setup(self):
        cglobals[ROOT_DIR] = str(Path(inspect.getfile(self._root.__class__)).parent.resolve())
        util.load_resources_dir(self._root.__class__)
        util.configure_logger(logging.INFO, APP_LOG)

    def _teardown(self):
        util.remove_signal_handlers()
        util.remove_logger()
        cglobals.reset()

    def __enter__(self):
        self._setup()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._teardown()
