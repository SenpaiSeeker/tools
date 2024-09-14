import logging, random, sys


class ColorfulFormatter(logging.Formatter):
    def format(self, record):
        color = random.choice(["\033[1;31m", "\033[1;32m", "\033[1;33m", "\033[1;34m", "\033[1;35m", "\033[1;36m", "\033[1;37m"])
        message = super().format(record)
        return f"{color}{message}\033[0m"

class LoggerHandler:
    def __init__(self, message: str = "[%(levelname)s] - %(name)s - %(message)s - %(asctime)s"):
        self.formatter = ColorfulFormatter(message)

    def logging(self, error_type=False):
        logging.basicConfig(
            level=logging.INFO,
            handlers=[logging.StreamHandler(sys.stdout)],
        )
        for handler in logging.getLogger().handlers:
            handler.setFormatter(self.formatter)

        if error_type:
            logging.getLogger("pyrogram").setLevel(logging.ERROR)
            logging.getLogger("asyncio").setLevel(logging.CRITICAL)


      
