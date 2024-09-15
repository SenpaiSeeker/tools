import logging
import random
import sys

COLORS = [
    "\033[1;91m",  # Merah Terang
    "\033[1;92m",  # Hijau Terang
    "\033[1;93m",  # Kuning Terang
    "\033[1;94m",  # Biru Terang
    "\033[1;95m",  # Ungu Terang
    "\033[1;96m",  # Cyan Terang
    "\033[1;97m",  # Putih Terangg
]
color = random.choice(COLORS)


class ColorfulFormatter(logging.Formatter):
    def format(self, record):
        message = super().format(record)
        return f"{color}{message}\033[0m"


class LoggerHandler:
    def __init__(self, format_str: str = "%(asctime)s: [%(levelname)s] - %(name)s - %(message)s"):
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
