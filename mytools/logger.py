import logging
import random
import sys


class ColorfulFormatter(logging.Formatter):
    COLORS = [
        "\033[1;91m",  # Merah Terang
        "\033[1;92m",  # Hijau Terang
        "\033[1;93m",  # Kuning Terang
        "\033[1;94m",  # Biru Terang
        "\033[1;95m",  # Ungu Terang
        "\033[1;96m",  # Cyan Terang
        "\033[1;97m",  # Putih Terang
        "\033[1;101m",  # Background Merah Terang
        "\033[1;102m",  # Background Hijau Terang
        "\033[1;103m",  # Background Kuning Terang
        "\033[1;104m",  # Background Biru Terang
        "\033[1;105m",  # Background Ungu Terang
        "\033[1;106m",  # Background Cyan Terang
        "\033[1;107m",  # Background Putih Terang
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
