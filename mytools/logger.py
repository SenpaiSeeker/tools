import logging
import random
import sys


class ColorfulFormatter(logging.Formatter):
    COLORS = [
        "\033[1;91;40m",  # Merah Terang dengan Background Hitam
        "\033[1;92;40m",  # Hijau Terang dengan Background Hitam
        "\033[1;93;40m",  # Kuning Terang dengan Background Hitam
        "\033[1;94;40m",  # Biru Terang dengan Background Hitam
        "\033[1;95;40m",  # Ungu Terang dengan Background Hitam
        "\033[1;96;40m",  # Cyan Terang dengan Background Hitam
        "\033[1;97;40m",  # Putih Terang dengan Background Hitam
        "\033[1;91;47m",  # Merah Terang dengan Background Putih
        "\033[1;92;47m",  # Hijau Terang dengan Background Putih
        "\033[1;93;47m",  # Kuning Terang dengan Background Putih
        "\033[1;94;47m",  # Biru Terang dengan Background Putih
        "\033[1;95;47m",  # Ungu Terang dengan Background Putih
        "\033[1;96;47m",  # Cyan Terang dengan Background Putih
        "\033[1;97;41m",  # Putih Terang dengan Background Merah Terang
        "\033[1;97;42m",  # Putih Terang dengan Background Hijau Terang
        "\033[1;97;43m",  # Putih Terang dengan Background Kuning Terang
        "\033[1;97;44m",  # Putih Terang dengan Background Biru Terang
        "\033[1;97;45m",  # Putih Terang dengan Background Ungu Terang
        "\033[1;97;46m",  # Putih Terang dengan Background Cyan Terang
        "\033[1;91;43m",  # Merah Terang dengan Background Kuning Terang
        "\033[1;92;44m",  # Hijau Terang dengan Background Biru Terang
        "\033[1;93;45m",  # Kuning Terang dengan Background Ungu Terang
        "\033[1;94;46m",  # Biru Terang dengan Background Cyan Terang
        "\033[1;95;41m",  # Ungu Terang dengan Background Merah Terang
        "\033[1;96;42m",  # Cyan Terang dengan Background Hijau Terang
        "\033[1;91;46m",  # Merah Terang dengan Background Cyan Terang
        "\033[1;92;41m",  # Hijau Terang dengan Background Merah Terang
        "\033[1;93;42m",  # Kuning Terang dengan Background Hijau Terang
        "\033[1;94;43m",  # Biru Terang dengan Background Kuning Terang
        "\033[1;95;44m",  # Ungu Terang dengan Background Biru Terang
        "\033[1;96;45m",  # Cyan Terang dengan Background Ungu Terang
        "\033[1;97;40m",  # Putih Terang dengan Background Hitam
        "\033[1;91;42m",  # Merah Terang dengan Background Hijau Terang
        "\033[1;92;43m",  # Hijau Terang dengan Background Kuning Terang
        "\033[1;93;44m",  # Kuning Terang dengan Background Biru Terang
        "\033[1;94;45m",  # Biru Terang dengan Background Ungu Terang
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
