import logging
import sys
import time 

COLORS = {
    "INFO": "\033[1;92m",  # Full Bright Green
    "DEBUG": "\033[1;94m",  # Full Bright Blue
    "WARNING": "\033[1;93m",  # Full Bright Yellow
    "ERROR": "\033[1;91m",  # Full Bright Red
    "CRITICAL": "\033[1;95m",  # Full Bright Magenta
    "RESET": "\033[0m",  # Reset color
}

class ColoredFormatter(logging.Formatter):
    def format(self, record):
        level_color = COLORS.get(record.levelname, COLORS.get('RESET'))
        record.levelname = f"{level_color}{record.levelname}{COLORS.get('RESET')}"
        return super().format(record)


class LoggerHandler:
    def __init__(self, log_level=logging.INFO):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)
        formatter = ColoredFormatter(
            "\033[1;97m[%(asctime)s] \033[1;96m| %(levelname)-9s \033[1;94m| %(module)s:%(funcName)s:%(lineno)d\033[0m %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)

    def send_message(self, log_type: str, message: str):
        log_function = getattr(self.logger, log_type.lower(), self.logger.warning)
        color = COLORS.get(log_type, COLORS["RESET"])
        log_function(f"{color}| {message}{COLORS['RESET']}")

log = LoggerHandler()

try:
    for log_type in ["INFO", "DEBUG", "WARNING", "ERROR", "CRITICAL"]:
        log.send_message(log_type, f"Iteration {log_type}: Halo World!")
        time.sleep(1)
except KeyboardInterrupt:
    log.send_message("WARNING", "Program dihentikan oleh pengguna.")
