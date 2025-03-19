import datetime
import logging
import os
from collections import deque
from pathlib import Path


class Logger(logging.Logger):

    def __init__(self, name=__name__, level=logging.INFO, file: str | bool = False, *args, **kwargs):
        """Change logger configuration here"""
        logging.basicConfig(encoding="utf-8")
        super().__init__(name=name, level=level, *args, **kwargs)
        format = "%(asctime)s %(levelname)+6s %(name)s %(filename)s(%(lineno)s): %(message)s"
        formatter = logging.Formatter(format, "%H:%M:%S")

        # Write logs to std
        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(formatter)
        self.addHandler(streamHandler)

        # Write logs to file
        if file:
            now = datetime.datetime.now()
            if file == True:
                logs_dir = Path("logs")
                logs_dir.mkdir(exist_ok=True)
                file = logs_dir

            if Path(file).is_dir():
                logs_dir = Path(file)
                file = logs_dir / (f'{name}_{now.strftime("%Y-%m-%d_%H-%M-%S")}.log')

            fileHandler = logging.FileHandler(file, encoding="utf-8")
            fileHandler.setFormatter(formatter)
            self.addHandler(fileHandler)


class _SingletonType(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(_SingletonType, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class SingletoneLogger(Logger, metaclass=_SingletonType):
    """Returnes the same instance every time"""

    def __init__(self, name=__name__, level=logging.INFO, file: str = False):
        super().__init__(name, level, file)


class LimitedLinesFileHandler(logging.FileHandler):
    """
    Limits max file length by trimming the file to max_lines lines.

    Usage:
    file_handler = LimitedLinesFileHandler("app_lock.log", mode="a", encoding="utf-8")
    """

    def __init__(self, filename, mode="a", encoding=None, delay=False, errors: str = None, max_lines=10_000):
        super().__init__(filename, mode, encoding, delay, errors)
        self.max_lines = max_lines

    def emit(self, record):
        super().emit(record)
        self._trim_file()

    def _trim_file(self):
        try:
            self.stream.flush()
            with open(self.baseFilename, "r", encoding=self.encoding) as f:
                # Use deque to keep only the last max_lines lines
                lines = deque(f, maxlen=self.max_lines)

            # Write the trimmed lines back to the file
            with open(self.baseFilename, "w", encoding=self.encoding) as f:
                f.writelines(lines)
        except Exception:
            self.handleError(None)


if __name__ == "__main__":
    # Set basic config
    logging.basicConfig(level=logging.DEBUG, encoding="utf-8")
    # Turn off specific logger
    logging.getLogger("aiogram").setLevel(logging.CRITICAL)
    # Usual logger
    logger = Logger()
    logger.error("Hello")
    logger = Logger("ytils.logger")
    logger.error("Hello 2")
    # Singletone logger
    logger = SingletoneLogger("singletone")
    logger.error("Hello 3")
    logger = SingletoneLogger("singletone2")
    logger.error("Hello 4")
