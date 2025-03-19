import logging
import time
from functools import wraps

from .logger import Logger

logger = Logger("ytils." + __name__)


def track_time(log_fun):
    def _track_time(fn):
        @wraps(fn)
        def wrapped_fn(*args, **kwargs):
            try:
                start_time = time.time()
                result = fn(*args, **kwargs)
            finally:
                elapsed_time = time.time() - start_time
                log_fun({"fn_name": fn.__name__, "elapsed_time": elapsed_time})
            return result

        return wrapped_fn

    return _track_time


class Profiler:

    def __init__(self, logger: logging.Logger = logger) -> None:
        self.logger = logger
        # CPU time.process_time()
        self._s = time.perf_counter()  # Start time
        self._m = self._s  # Marker for time since the last trace

    def restart(self):
        self._s = time.perf_counter()
        self._m = self._s

    def trace(self, text: str, restart=False):
        current_time = time.perf_counter()
        elapsed_since_start = current_time - self._s
        elapsed_since_marker = current_time - self._m
        self.logger.debug(f"Profiler:{text.rjust(50)}: {elapsed_since_marker:.5f} total: {elapsed_since_start:.5f}")
        self._m = current_time
        if restart == True:
            self.restart()


@track_time(lambda message: logger.info("{elapsed_time:.3f}s > {fn_name}".format(**message)))
def _test_track_time():
    time.sleep(5)


def _test_profiler():
    profiler = Profiler()
    time.sleep(3)
    profiler.trace("1")
    time.sleep(5)
    profiler.trace("2", restart=True)
    time.sleep(2)
    profiler.trace("3", restart=True)


if __name__ == "__main__":
    _test_track_time()
    _test_profiler()
