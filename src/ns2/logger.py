"""Logger module for logging messages to the console."""
import os
import logging
import inspect
from rich.console import Console
from rich.logging import RichHandler
from rich.text import Text


class CustomFormatter(logging.Formatter):
    """Custom Formatter to include caller file name and line number."""

    _log_format = "%(asctime)s - %(levelname)s - [%(file_name)s:%(line_number)03d] - %(message)s"

    def format(self, record):
        """Format the log record."""
        # Get the file name and line number of the caller
        self.get_line_info(record)

        # Use the custom log format
        formatter = logging.Formatter(self._log_format)
        return formatter.format(record)

    def get_line_info(self, record):
        """Extract and set the caller's file name and line number in the record."""
        caller_info = self._get_caller_info()
        record.file_name = caller_info[0]  # Add file name to the log record
        # Add line number to the log record
        record.line_number = caller_info[1]

    def _handle_filename(self, filename):
        """
        Simplify the filename to display only the relevant part.

        Args:
            filename (str): Full path of the file.

        Returns:
            str: Simplified file name.
        """

        path_delimiter = "\\" if os.name == "nt" else "/"
        search_term = "Nordstream2"+path_delimiter+"src"+path_delimiter

        if search_term in filename:
            # Keep only the part after "src\ns2" and remove the rest
            filename = filename.split(search_term, 1)[-1]
            # Remove leading slashes or backslashes
            if filename.startswith("\\") or filename.startswith("/"):
                filename = filename[1:]
        return filename

    def _get_caller_info(self):
        """
        Get the filename and line number of the actual caller.

        Returns:
            tuple: A tuple containing the filename and line number of the caller.
        """
        stack = inspect.stack()
        # Skip the first frames related to logging
        for frame in stack:
            module = inspect.getmodule(frame[0])
            # Skip frames from this logger module or the logging module itself
            if module and module.__name__ not in ("logging", __name__, "rich.logging"):
                filename = frame.filename  # Full path of the file
                filename = self._handle_filename(
                    filename)  # Simplify the file name
                line_number = frame.lineno  # Line number in the file
                return filename, line_number
        return "unknown", 0  # Default if no valid frame is found


class CustomLogger:
    """
    A custom logger class that supports logging to the console.
    Console messages are styled using Rich for better readability.
    """

    def __init__(self, log_level=logging.INFO, name="CustomLogger"):
        """
        Initialize the CustomLogger.

        Args:
            log_level (int): Logging level. Default is logging.INFO.
        """
        self.console = Console()
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)

        # Setup console handler
        self._setup_console_handler(log_level)

    def _setup_console_handler(self, log_level):
        """
        Setup the Rich console handler.

        Args:
            log_level (int): Logging level for the console handler.
        """
        console_handler = RichHandler(
            console=self.console,
            level=log_level,
            show_path=False
        )
        console_handler.setFormatter(CustomFormatter())
        self.logger.addHandler(console_handler)

    def debug(self, message):
        """
        Log a debug message (custom log level).

        :param message: The message to log.
        :type message: str
        :return: None
        """
        self.logger.debug(message)

    def _log_message(self, level, message, success=False):
        """
        Log a message with the specified level.
        If success is set to True, the message will be styled as a success message
        in bold green text via Rich.
        """
        if success:
            message = Text(f"[SUCCESS] {message}", style="bold green")
        else:
            message = Text(message)
        self.logger.log(level, message)

    def info(self, message, success=False):
        """
        Log an info message (custom log level).

        :param message: The message to log.
        :type message: str
        :return: None
        """
        self._log_message(logging.INFO, message, success)

    def warning(self, message):
        """
        Log an warning message (custom log level).

        :param message: The message to log.
        :type message: str
        :return: None
        """
        self.logger.warning(message)

    def error(self, message):
        """
        Log an error message (custom log level).

        :param message: The message to log.
        :type message: str
        :return: None
        """
        self.logger.error(message)

    def critical(self, message):
        """
        Log a critical message (custom log level).

        :param message: The message to log.
        :type message: str
        :return: None
        """
        self.logger.critical(message)

    def success(self, message):
        """
        Log a success message (custom log level).

        :param message: The message to log.
        :type message: str
        :return: None
        """
        self.logger.log(logging.INFO, "[SUCCESS] %s", message)
