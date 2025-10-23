"""Main module for the Todo command-line application."""

import sys as system
import argparse

# Local import
from .todo import run_todo_app
from .logger import TodoLogger


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse and return command-line arguments for the Todo application.

    Configures all available command-line options for managing tasks, debugging,
    and controlling output behavior.

    Args:
        argv (list[str] | None): Command-line arguments (usually ``sys.argv[1:]``).

    Returns:
        argparse.Namespace: Parsed command-line arguments containing all user options.

    Options:
        -a, --add TEXT          Add a new task with the given description.
        -l, --list              List all tasks (optionally filtered by --completed, --pending, or --category).
        -c, --complete ID       Mark a task as completed by its ID.
        -d, --delete ID         Delete a task by its ID.
        -C, --category NAME     Filter or assign a category to a task.
        -p, --priority LEVEL    Specify or filter by priority (Low, Med, High).
        --due DATE              Specify a due date (format: YYYY-MM-DD).
        --completed             Show only completed tasks.
        --pending               Show only pending tasks.
        -f, --file PATH         Specify a custom JSON file for task storage.
        --debug                 Enable debug mode with verbose logging.
        --version               Show application version information and exit.
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
    parser.add_argument("--version", "-v", action="version", version="Todo App 0.1.0")

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
