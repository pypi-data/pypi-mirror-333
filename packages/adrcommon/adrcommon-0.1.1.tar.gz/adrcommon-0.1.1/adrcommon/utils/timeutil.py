import asyncio
import logging
import time
from datetime import datetime
from functools import partial
from threading import Thread, Timer
from typing import Callable, Any, Coroutine

LOGGER = logging.getLogger(__name__)


def epoch_time(dt: datetime = None) -> int:
    dt = dt or datetime.now()
    return int(round(dt.timestamp() * 1000))


class Timed:
    def __init__(self):
        self._start = 0
        self._end = 0

    def start(self):
        self._start = time.time()

    def end(self):
        self._end = time.time()

    def total(self):
        return self._end - self._start

    def __str__(self):
        return f'{self.total():.2f}'

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end()


class Interval:
    def __init__(self, name: str, interval: float, function, args=None, kwargs=None):
        args = args or []
        kwargs = kwargs or {}

        self._name = name
        self._interval = self._remainder = interval
        self._function = partial(function, *args, **kwargs)
        self._force_stop = False
        self._timer = None

    def __call__(self):
        if self._force_stop: return

        with Timed() as t:
            try: self._function()  # call the partial function
            except Exception as e:
                LOGGER.exception('Error running interval function', exc_info=e)

        # if stop was called while function was running, detect it before
        # scheduling next run
        if self._force_stop: return
        self._schedule_next_run(t.total())

    def _schedule_next_run(self, time_diff):
        self._remainder = self._interval - time_diff
        self._remainder = self._remainder if self._remainder > 0 else 0
        self.start()

    def start(self, run_now=False):
        timeout = 0 if run_now else self._remainder

        self._timer = Timer(timeout, self)
        self._timer.name = self._name
        self._timer.start()

    def stop(self):
        if self._timer:
            self._timer.cancel()
        self._timer = None

        self._force_stop = True
