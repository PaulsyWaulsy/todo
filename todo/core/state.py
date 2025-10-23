"""Application state management for the Todo application."""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from pathlib import Path
from todo.utils.logger import TodoLogger
import time


@dataclass
class TodoState:
    """Global runtime state for the Todo application.

    The AppState class serves as a structured container for runtime
    configuration, parsed CLI arguments, and transient data used across
    the application. It centralizes access to shared context, reducing
    reliance on global variables and simplifying debugging.

    Attributes:
        args (Any): Parsed command-line arguments (e.g., from argparse).
        debug (bool): Whether debug mode is enabled.
        start_time (float): Epoch timestamp representing when the
            application was started.
        logger (logging.Logger): Configured logger instance for the app.
    """

    args: argparse.Namespace
    debug: bool = False
    start_time: float = field(default_factory=time.time)
    logger: TodoLogger = field(init=False)

    def __post_init__(self) -> None:
        """Perform post-initialization setup.

        Sets the debug flag and data file path based on CLI arguments
        (if provided) and initializes the logger.
        """
        if hasattr(self.args, "debug"):
            self.debug = bool(self.args.debug)

        if hasattr(self.args, "file") and self.args.file:
            self.data_file = Path(self.args.file)

        self.logger = TodoLogger()
        self.logger.info(f"Using data file: {self.data_file}")

    def uptime(self) -> float:
        """Return the time elapsed since the application started.

        Returns:
            float: Number of seconds since initialization.
        """
        return time.time() - self.start_time
