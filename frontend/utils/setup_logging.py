import logging
import sys

import loguru


class LoguruHandler(logging.Handler):
    """Хэндлер передающий сообщения из logging в loguru"""

    def __init__(self, sink):  # type: ignore
        super().__init__()
        self.logger = sink

    loglevel_mapping = {
        50: "CRITICAL",
        40: "ERROR",
        30: "WARNING",
        20: "INFO",
        10: "DEBUG",
        0: "NOTSET",
    }

    def emit(self, record: logging.LogRecord):
        try:
            level = self.logger.level(record.levelname).name
        except AttributeError:
            level = self.loglevel_mapping[record.levelno]

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back  # type: ignore
            depth += 1

        self.logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def setup_logging(level: str = "INFO", _logger=loguru.logger) -> logging.Logger:  # type: ignore
    """Отдает объект логгинга loguru и обновляет хэндлеры уже существующим логгерам uvicorn и fastapi"""  # noqa
    # удаляем стандартный хэндлер, добавляемый при инициализации loguru
    _logger.remove()
    _logger.add(
        sys.stderr,
        level=level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss Z}</green> | " "<level>{level}</level> | {message}",
    )
    # intercept everything at the root logger
    logging.root.handlers = [LoguruHandler(_logger)]
    logging.root.setLevel(level)

    # remove every other logger's handlers
    # and propagate to root logger
    for name in logging.root.manager.loggerDict.keys():  # noqa
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True

    return _logger
