import sys
import datetime
from .formatters import DefaultFormatter


class StdoutLogger:
    """
    A simple logger that outputs to stdout with customizable formatters.
    """

    LEVELS = {
        "debug": 10,
        "info": 20,
        "warning": 30,
        "error": 40,
        "critical": 50,
    }

    def __init__(self, formatter=None, level="info"):
        """
        Initialize the StdoutLogger.

        Args:
            formatter: A formatter object that implements format_message method.
                       Defaults to DefaultFormatter.
            level: Minimum log level to display. Defaults to "info".
        """
        self.formatter = formatter or DefaultFormatter()
        self.level = self.LEVELS.get(level.lower(), 20)

    def set_level(self, level):
        """Set the minimum log level."""
        self.level = self.LEVELS.get(level.lower(), self.level)

    def log(self, level, message, **kwargs):
        """
        Log a message at the specified level.

        Args:
            level: The log level ("debug", "info", "warning", "error", "critical")
            message: The message to log
            **kwargs: Additional context to include in the log message
        """
        level_num = self.LEVELS.get(level.lower(), 0)
        if level_num >= self.level:
            context = {
                "level": level,
                "message": message,
                "time": datetime.datetime.now(),
                **kwargs,
            }
            formatted_message = self.formatter.format_message(context)
            print(formatted_message, file=sys.stdout)

    def debug(self, message, **kwargs):
        """Log a debug message."""
        self.log("debug", message, **kwargs)

    def info(self, message, **kwargs):
        """Log an info message."""
        self.log("info", message, **kwargs)

    def warning(self, message, **kwargs):
        """Log a warning message."""
        self.log("warning", message, **kwargs)

    def error(self, message, **kwargs):
        """Log an error message."""
        self.log("error", message, **kwargs)

    def critical(self, message, **kwargs):
        """Log a critical message."""
        self.log("critical", message, **kwargs)
