import logging
import sys

COLORS = {
    "INFO": "\033[1;92m",  # Full Bright Green
    "DEBUG": "\033[1;94m",  # Full Bright Blue
    "WARNING": "\033[1;93m",  # Full Bright Yellow
    "ERROR": "\033[1;91m",  # Full Bright Red
    "CRITICAL": "\033[1;95m",  # Full Bright Magenta
    "RESET": "\033[0m",  # Reset color
}


class LoggerHandler:
    def __init__(self, name: str = __name__, log_level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)
        formatter = logging.Formatter(
            "\033[1;97m[%(asctime)s] \033[1;96m| %(levelname)-9s \033[1;94m| %(module)s:%(lineno)s\033[0m %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
         )
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)

    def send_message(self, log_type: str, message: str):
        log_function = getattr(self.logger, log_type.lower(), self.logger.warning)
        color = COLORS.get(log_type, COLORS["RESET"])
        log_function(f"{color}| {message}{COLORS['RESET']}")

