"""Logger for visualizing and distinguishing message types."""

INFO_COLOR = "\033[94m"  # Blue
WARN_COLOR = "\033[93m"  # Yellow
ERROR_COLOR = "\033[91m"  # Red
SUCCESS_COLOR = "\033[92m"  # Green
RESET = "\033[0m"


class TodoLogger:
    """Lightweight color logger for console output.

    Provides simple, colored log messages for CLI feedback. This replaces
    the need for Python’s built-in logging module in small CLI apps.

    Methods:
        info(msg): Print informational message in blue.
        warn(msg): Print warning message in yellow.
        error(msg): Print error message in red.
        success(msg): Print success message in green.
    """

    def info(self, msg: str) -> None:
        """Print an informational message in blue.

        Args:
            msg (str): Message text to display.
        """
        print(f"[{INFO_COLOR}INFO{RESET}] {msg}")

    def warn(self, msg: str) -> None:
        """Print a warning message in yellow.

        Args:
            msg (str): Message text to display.
        """
        print(f"[{WARN_COLOR}WARN{RESET}] {msg}")

    def error(self, msg: str) -> None:
        """Print an error message in red.

        Args:
            msg (str): Message text to display.
        """
        print(f"[{ERROR_COLOR}ERROR{RESET}] {msg}")

    def success(self, msg: str) -> None:
        """Print a success message in green.

        Args:
            msg (str): Message text to display.
        """
        print(f"[{SUCCESS_COLOR}OK{RESET}] {msg}")
