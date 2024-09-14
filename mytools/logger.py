import logging
import random
import sys


class ColorfulFormatter(logging.Formatter):
    COLORS = [
        "\033[1;31m",
        "\033[1;32m",
        "\033[1;33m",
        "\033[1;34m",
        "\033[1;35m",
        "\033[1;36m",
        "\033[1;37m",
    ]

    def format(self, record):
        color = random.choice(self.COLORS)
        message = super().format(record)
        return f"{color}{message}\033[0m"


class LoggerHandler:
    def __init__(self, format_str: str = "[%(levelname)s] - %(name)s - %(message)s - %(asctime)s"):
        self.formatter = ColorfulFormatter(format_str)

    def setup_logger(self, error_logging: bool = False, log_level=logging.INFO):
        logging.basicConfig(level=log_level, handlers=[logging.StreamHandler(sys.stdout)])
        for handler in logging.getLogger().handlers:
            handler.setFormatter(self.formatter)

        if error_logging:
            logging.getLogger("pyrogram").setLevel(logging.ERROR)
            logging.getLogger("asyncio").setLevel(logging.CRITICAL)

    def get_logger(self, name: str):
        return logging.getLogger(name)
