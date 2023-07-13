from __future__ import annotations

import logging
from logging import Formatter, LogRecord

import coloredlogs


class Color:
    COLORS: dict = {
        'red': 31,
        'green': 32,
        'yellow': 33,
        'cyan': 36,
        'white': 37,
        'bgred': 41,
        'bggrey': 100
    }
    PREFIX: str = '\033['
    SUFFIX: str = '\033[0m'

    def colored(self, text: str, color: str | None = None) -> str:
        if color not in self.COLORS:
            color = 'white'

        clr = self.COLORS[color]
        return (self.PREFIX + '%dm%s' + self.SUFFIX) % (clr, text)


colored = Color().colored


class ColoredFormatter(Formatter):
    def format(self, record: LogRecord) -> str:
        message = record.getMessage()

        mapping = {
            'DEBUG': 'bggrey',
            'INFO': 'cyan',
            'SUCCESS': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bgred',
        }

        clr = mapping.get(record.levelname, 'white')

        return colored(record.levelname, clr) + ': ' + message


def set_logging() -> None:
    logging.SUCCESS = 25
    logging.addLevelName(logging.SUCCESS, 'SUCCESS')
    logging.success = lambda message, *args: logging.log(logging.SUCCESS, message, *args)

    coloredlogs.install(fmt='%(levelname)-8s | %(message)s', level="INFO")
