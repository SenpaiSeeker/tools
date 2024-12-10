import logging
import sys

COLORS = [
    "\033[1;91m",
    "\033[1;92m",
    "\033[1;93m",
    "\033[1;94m",
    "\033[1;95m",
    "\033[1;96m",
    "\033[1;97m",
]


class LoggerHandler:
    def __init__(
        self,
        name: str = __name__,
        format_str: str = "{0}[%(asctime)s] {1}| {2}%(levelname)-9s {1}| {3}%(module)s:%(lineno)d {1}| {4}%(message)s\033[0m"
    ):
        self.name = name
        self.format_str = format_str.format(COLORS[6], COLORS[4], COLORS[5], COLORS[3], COLORS[1])
        self.setup = self.setup_logger()

    def setup_logger(self, error_logging: bool = False, log_level=logging.INFO):
        formatter = logging.Formatter(self.format_str, datefmt="%Y-%m-%d %H:%M:%S")
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)

        logger = logging.getLogger(self.name)
        logger.setLevel(log_level)
        logger.addHandler(stream_handler)

        if error_logging:
            logging.getLogger("pyrogram").setLevel(logging.ERROR)
            logging.getLogger("asyncio").setLevel(logging.CRITICAL)

        return logger

    def send_message(self, log_type: str, message: str):
        logger = logging.getLogger(self.name)

        log_types = {
            "INFO": self.colorize_log("INFO", logger.info),
            "DEBUG": self.colorize_log("DEBUG", logger.debug),
            "WARNING": self.colorize_log("WARNING", logger.warning),
            "ERROR": self.colorize_log("ERROR", logger.error),
            "CRITICAL": self.colorize_log("CRITICAL", logger.critical),
        }

        if log_type in log_types:
            log_types[log_type](message)
        else:
            logger.warning(f"Invalid log type: {log_type}. Message: {message}")

    def colorize_log(self, level: str, log_function):
        color_map = {
            "INFO": COLORS[1],
            "DEBUG": COLORS[3],
            "WARNING": COLORS[2],
            "ERROR": COLORS[0],
            "CRITICAL": COLORS[4],
        }
        color = color_map.get(level, COLORS[1])

        def log_with_color(message):
            log_function(f"{color}{message}\033[0m")

        return log_with_color
