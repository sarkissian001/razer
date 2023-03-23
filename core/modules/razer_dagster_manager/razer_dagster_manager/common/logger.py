import logging
import sys
from typing import Union


class Logger:
    def __init__(self, name: str, level_name: Union[str, None] = None) -> None:
        if not level_name:
            level_name = "DEBUG"

        self.level: int = self._get_level(level_name)

        self.logger = logging.getLogger(name)
        self.logger.setLevel(self.level)
        self.handler = logging.StreamHandler(sys.stderr)
        self.handler.setLevel(self.level)
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s", "%Y-%m-%dT%H:%M:%SZ"
        )
        self.handler.setFormatter(formatter)
        self.logger.addHandler(self.handler)

    @staticmethod
    def _get_level(level_name: str) -> int:
        level = getattr(logging, level_name.upper(), logging.NOTSET)
        return level

    def error(self, message, *args):
        self.logger.error(message, *args)

    def info(self, message, *args):
        self.logger.info(message, *args)

    def debug(self, message, *args):
        self.logger.debug(message, *args)

    def critical(self, message, *args):
        self.logger.critical(message, *args)

    def warning(self, message, *args):
        self.logger.warning(message, *args)
