import sys
import datetime
from .formatters import DefaultFormatter


class StdoutLogger:
    """
    A flexible logger that outputs to stdout with customizable formatters.
    Includes support for module name and hash string identifiers.
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

    def set_level(self, level: str):
        """Set the minimum log level."""
        self.level = self.LEVELS.get(level.lower(), self.level)

    def log(self, level: str, module: str, hash_id: str, message: str, **kwargs):
        """
        Log a message at the specified level with module name and hash identifiers.

        Args:
            level: The log level ("debug", "info", "warning", "error", "critical")
            module: Identifier for the module generating the log
            hash_id: Hash identifier (e.g., MD5, transaction ID, etc.)
            message: The message to log
            **kwargs: Additional context to include in the log message
        """
        level_num = self.LEVELS.get(level.lower(), 0)
        if level_num >= self.level:
            context = {
                "level": level,
                "module": module,
                "hash_id": hash_id,
                "message": message,
                "time": datetime.datetime.now(),
                **kwargs,
            }
            formatted_message = self.formatter.format_message(context)
            print(formatted_message, file=sys.stdout)

    def debug(self, module: str, hash_id: str, message: str, **kwargs):
        """Log a debug message with module name and hash string."""
        self.log("debug", module, hash_id, message, **kwargs)

    def info(self, module: str, hash_id: str, message: str, **kwargs):
        """Log an info message with module name and hash string."""
        self.log("info", module, hash_id, message, **kwargs)

    def warning(self, module: str, hash_id: str, message: str, **kwargs):
        """Log a warning message with module name and hash string."""
        self.log("warning", module, hash_id, message, **kwargs)

    def error(self, module: str, hash_id: str, message: str, **kwargs):
        """Log an error message with module name and hash string."""
        self.log("error", module, hash_id, message, **kwargs)

    def critical(self, module: str, hash_id: str, message: str, **kwargs):
        """Log a critical message with module name and hash string."""
        self.log("critical", module, hash_id, message, **kwargs)
