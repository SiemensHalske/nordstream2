import inspect
import os


class CustomLogger:
    """
    A minimal logger class for demonstrating _get_caller_info functionality.
    """

    def _get_caller_info(self):
        """
        Get the filename and line number of the actual caller.

        Returns:
            tuple: A tuple containing the filename and line number of the caller.
        """

        print("Getting caller info")

        stack = inspect.stack()
        for frame in stack[2:]:
            filename = os.path.basename(frame.filename)
            line_number = frame.lineno
            return filename, line_number
        return "unknown", 0

    def log_to_console(self, message):
        """
        Log a message to the console with caller information.

        Args:
            message (str): The message to log.
        """
        relative_path, line_number = self._get_caller_info()
        print(f"{message} (called from {relative_path}:{line_number})")


class CallerLogger:
    """
    A class that uses CustomLogger to log messages with caller information.
    """

    def __init__(self):
        self.logger = CustomLogger()

    def log_message(self, message):
        """
        Log a message using the CustomLogger.

        Args:
            message (str): The message to log.
        """
        self.logger.log_to_console(message)

    def another_method(self):
        """
        Demonstrates logging from a different method.
        """
        self.logger.log_to_console("Message from another method.")


# Example usage
if __name__ == "__main__":
    # Create an instance of CallerLogger
    caller_logger = CallerLogger()

    # Log a message from one method
    caller_logger.log_message("This is a message from log_message.")

    # Log a message from another method
    caller_logger.another_method()
