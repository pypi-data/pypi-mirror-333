import logging
import coloredlogs
from colored import Fore, Style

class Debug:
    """Handles logging with colored output for better visibility."""

    @staticmethod
    def log(message: str, level='INFO'):
        """Logs a message with a specified severity level and colored output.

        Args:
            message (str): The message to log.
            level (str, optional): The log level (INFO, DEBUG, ERROR, etc.). Defaults to "INFO".
        """

        logger = logging.getLogger("SnowforgeLogger")

        # Ensure logger has a handler
        if not logger.hasHandlers():
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
            logger.addHandler(handler)

        level = level.upper()
        log_levels = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }
        logger.setLevel(log_levels.get(level, logging.INFO))

        # Define color mapping
        color_map = {
            'INFO': Fore.white,
            'ERROR': Fore.red,
            'DEBUG': Fore.blue,
            'WARNING': Fore.yellow,
            'SUCCESS': Fore.light_green,
            'FAILURE': Fore.red,
            'CRITICAL': Fore.light_red
        }

        colored_message = f"{color_map.get(level, Fore.white)}{message}{Style.reset}"

        if level in log_levels:
            getattr(logger, level.lower())(colored_message)
        else:
            logger.info(colored_message)
