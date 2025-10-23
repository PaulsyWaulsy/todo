"""Main module for the Todo command-line application."""

import sys as system
import argparse

# Local import
from .todo import run_todo_app
from .logger import TodoLogger


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse and return command-line arguments for the Todo application.

    Configures available command-line options for managing tasks, debugging,
    and controlling output behavior.

    Args:
        argv: Command-line arguments (usually sys.argv[1:]).

    Returns:
        argparse.Namespace: Parsed command-line arguments.

    Available Options:
        --add, -a           Add a new task.
        --list, -l          List all tasks (can be filtered with --completed or --pending).
        --complete, -c ID   Mark a task as completed by ID.
        --delete, -d ID     Delete a task by ID.
        --category, -C CAT  Filter or assign category to a task.
        --debug             Enable debug mode for verbose logging.
        --file, -f PATH     Specify custom todo storage file.
        --version, -v       Show version information.
    """
    parser = argparse.ArgumentParser(description="Command-line Todo application")

    # Core actions
    parser.add_argument("-a", "--add", help="Add a new task (provide description)", type=str)
    parser.add_argument("-l", "--list", action="store_true", help="List all tasks")
    parser.add_argument("-c", "--complete", type=str, help="Mark a task as completed by ID")
    parser.add_argument("-d", "--delete", type=str, help="Delete a task by ID")

    # Additional options
    parser.add_argument(
        "-p",
        "--priority",
        type=str,
        choices=["Low", "Med", "High"],
        help="Specify the priority for a new task or filter by priority",
    )

    parser.add_argument(
        "--due",
        type=str,
        help="Specify due date (format: YYYY-MM-DD)",
    )

    # Filters and categories
    parser.add_argument("-C", "--category", type=str, help="Filter or assign category")
    parser.add_argument("--completed", action="store_true", help="Show only completed tasks")
    parser.add_argument("--pending", action="store_true", help="Show only pending tasks")

    # Configuration
    parser.add_argument("-f", "--file", type=str, default="todo.json", help="Path to storage file")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("--version", "-v", action="version", version="Todo App 1.0")

    return parser.parse_args(argv)


def validate_args(args: argparse.Namespace) -> None:
    """Validate parsed command-line arguments.

    Args:
        args (argparse.Namespace): Parsed command-line arguments.
    """
    if args.completed and args.pending:
        raise ValueError("Cannot use --completed and --pending filters together.")


def main(argv: list[str] | None = None) -> int:
    """Main function.

    Args:
        argv: Command-line arguments (usually sys.argv[1:]).
    """
    args = parse_args(argv)
    try:
        validate_args(args)
    except ValueError as error:
        TodoLogger().error(str(error))
        return 1

    run_todo_app(args)
    return 0


if __name__ == "__main__":
    main(system.argv[1:])
