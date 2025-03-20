import inspect
import logging
import signal
from pathlib import Path

from adrcommon import constants
from .cglobals import cglobals


def get_make_dir(path: Path) -> Path:
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)

    return path

def get_root_dir() -> Path:
    return cglobals[constants.ROOT_DIR]

def get_resources_dir():
    return Path(cglobals[constants.RESOURCES])

def load_resources_dir(cls):
    fs_root = Path(Path.cwd().root)
    start_dir = Path(inspect.getfile(cls)).parent

    while not fs_root.samefile(start_dir):
        if start_dir.joinpath(constants.RESOURCES) in start_dir.iterdir():
            cglobals[constants.RESOURCES] = str(start_dir.joinpath(constants.RESOURCES).resolve())
            return

        start_dir = start_dir.parent

    cglobals[constants.RESOURCES] = None

def get_work_dir(rel_path=None) -> Path:
    work_dir = cglobals.get(constants.WORK_DIR, Path(get_root_dir(), constants.WORK))
    path = get_make_dir(work_dir)

    if rel_path:
        path = get_make_dir(Path(path, rel_path))

    return path

def set_work_dir(path: Path):
    if not path: return
    del cglobals[constants.WORK_DIR]
    cglobals[constants.WORK_DIR] = path

def get_work_file(rel_path) -> Path:
    return Path(get_work_dir(), rel_path)

def get_data_dir() -> Path:
    return get_work_dir(constants.DATA)

def get_data_file(rel_path) -> Path:
    return Path(get_data_dir(), rel_path)

def configure_logger(log_level, log_name):
    log_file = Path(get_log_dir(), log_name)
    
    handlers = logging.getLogger().handlers
    for handler in handlers:
        logging.getLogger().removeHandler(handler)

    log_out = logging.FileHandler(filename=log_file)
    log_out.setLevel(log_level)
    log_out.setFormatter(logging.Formatter(constants.LOG_FORMAT))

    logging.getLogger().addHandler(log_out)
    logging.getLogger().setLevel(log_level)

def remove_logger():
    logging.shutdown()

def get_log_dir() -> Path:
    return get_work_dir(constants.LOG)

def get_log_file(log_name):
    return Path(get_log_dir(), log_name)

def add_signal_handlers(handler):
    h = lambda *args: handler()
    for sgnl in [signal.SIGINT, signal.SIGTERM]:
        signal.signal(sgnl, h)

def remove_signal_handlers():
    for sgnl in [signal.SIGINT, signal.SIGTERM]:
        signal.signal(sgnl, signal.SIG_DFL)
