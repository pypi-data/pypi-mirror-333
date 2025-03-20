import datetime
import json


class DefaultFormatter:
    """
    Default formatter for log messages.
    Format: [LEVEL] YYYY-MM-DD HH:MM:SS - [MODULE] [HASH] Message
    """

    def format_message(self, context):
        """
        Format the log message using the provided context.

        Args:
            context: A dictionary containing logging context information
                     (level, message, module, hash_id, time, and any additional fields)

        Returns:
            The formatted log message string
        """
        time_str = context["time"].strftime("%Y-%m-%d %H:%M:%S")
        level_str = context["level"].upper()
        module_str = context.get("module", "")
        hash_id = context.get("hash_id", "")

        return f"[{level_str}] {time_str} - [{module_str}] [{hash_id}] {context['message']}"


class ColoredFormatter(DefaultFormatter):
    """
    Formatter that adds color to the log messages based on level.
    """

    COLORS = {
        "debug": "\033[36m",  # Cyan
        "info": "\033[32m",  # Green
        "warning": "\033[33m",  # Yellow
        "error": "\033[31m",  # Red
        "critical": "\033[35m",  # Magenta
    }
    RESET = "\033[0m"

    def format_message(self, context):
        """Format the log message with color based on level."""
        level = context["level"].lower()
        color = self.COLORS.get(level, "")
        formatted_message = super().format_message(context)
        return f"{color}{formatted_message}{self.RESET}"


class JsonFormatter:
    """
    Formatter that outputs log messages in JSON format.
    Includes all context fields, making it ideal for machine processing.
    """

    def format_message(self, context):
        """Format the log message as JSON."""
        # Create a copy of the context
        json_context = context.copy()

        # Convert datetime objects to ISO format strings
        if isinstance(json_context.get("time"), datetime.datetime):
            json_context["time"] = json_context["time"].isoformat()

        # Convert any other non-serializable objects
        for key, value in json_context.items():
            if not isinstance(value, (str, int, float, bool, list, dict, type(None))):
                json_context[key] = str(value)

        # Ensure level is always uppercase in JSON
        json_context["level"] = json_context["level"].upper()

        return json.dumps(json_context)


class CustomFormatter:
    """
    Formatter that allows custom format strings.

    Format string can include {level}, {message}, {module}, {hash_id},
    {time}, and any other keys that might be in the context dictionary.
    """

    def __init__(self, format_string="{level} - {message}"):
        """
        Initialize the CustomFormatter.

        Args:
            format_string: A string with placeholders to be replaced by context values.
        """
        self.format_string = format_string

    def format_message(self, context):
        """Format the log message using the custom format string."""
        # Create a copy of the context with level uppercase
        format_context = context.copy()
        format_context["level"] = context["level"].upper()

        # Format time if it's a datetime object
        if isinstance(context.get("time"), datetime.datetime):
            format_context["time"] = context["time"].strftime("%Y-%m-%d %H:%M:%S")

        # Replace placeholders in the format string
        result = self.format_string
        for key, value in format_context.items():
            placeholder = f"{{{key}}}"
            if placeholder in result:
                result = result.replace(placeholder, str(value))

        return result
