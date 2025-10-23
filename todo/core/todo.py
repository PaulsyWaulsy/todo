"""Todo application logic and runtime orchestration."""

from __future__ import annotations

import argparse
from pathlib import Path

from todo.core.state import TodoState
from todo.data.storage import TodoStorage, generate_todo_id
from todo.models.record import TodoRecord
from datetime import datetime

HIGH_COLOR = "\033[91m"  # Red
MED_COLOR = "\033[93m"  # Yellow
LOW_COLOR = "\033[92m"  # Green
RESET_COLOR = "\033[0m"


def run_todo_app(args: argparse.Namespace) -> None:
    """Run the main Todo application workflow.

    This function acts as the primary entry point for executing the Todo
    app logic. It initializes global state, handles command-line actions,
    and coordinates data persistence through the TodoStorage system.

    Args:
        args (argparse.Namespace): Parsed command-line arguments from the CLI.

    Returns:
        None
    """
    state = TodoState(args)
    storage = TodoStorage(root=Path("data"))

    if state.debug:
        state.logger.info("Starting Todo Application")

    if args.add:
        handle_add_task(state, storage, args)
    elif args.list or args.completed or args.pending:
        handle_list_tasks(state, storage, args)
    elif args.complete:
        handle_mark_complete(state, storage, args.complete)
    elif args.delete:
        handle_delete_task(state, storage, args.delete)
    else:
        state.logger.warn("No action specified. Use --help for usage info.")


def handle_add_task(state: TodoState, storage: TodoStorage, args: argparse.Namespace) -> None:
    """Add a new todo task and persist it.

    Args:
        state (TodoState): Current application state.
        storage (TodoStorage): Persistent storage handler.
        description (str): Description of the todo item.
        args (argparse.Namespace): Parsed command-line arguments from the CLI.

    Returns:
        None
    """
    category = args.category
    priority = args.priority

    due_date = None
    if args.due:
        try:
            due_date = datetime.strptime(args.due, "%Y-%m-%d")
        except ValueError:
            state.logger.warn("Invalid due date format. Use YYYY-MM-DD.")

    todo = TodoRecord(
        id=generate_todo_id(),
        created_at=datetime.now(),
        completed=False,
        category=[category] if category else [],
        priority=priority,
        due_date=due_date,
        description=args.add,
        folder=Path("data"),
    )

    storage.add_todo(todo)
    state.logger.success(f"Added new task: '{args.add}'")


def _filtered_list(
    state: TodoState, storage: TodoStorage, args: argparse.Namespace
) -> list[TodoRecord] | None:
    """Filter and return a list of todo tasks based on CLI arguments.

    Args:
        state (TodoState): Current application state.
        storage (TodoStorage): Persistent storage handler.
        args (argparse.Namespace): Parsed command-line arguments.

    Returns:
        list[TodoRecord] | None: Filtered list of todo tasks or None if no tasks found.
    """
    todos = storage.load_todos()

    if not todos:
        state.logger.info("No tasks found.")
        return

    # Determine filtering context
    show_completed = getattr(args, "completed", False)
    show_pending = getattr(args, "pending", False)
    category_filter = getattr(args, "category", None)
    priority_filter = getattr(args, "priority", None)

    if show_completed:
        state.logger.info("Listing completed tasks:")
    elif show_pending:
        state.logger.info("Listing pending tasks:")
    elif category_filter:
        state.logger.info(f"Listing tasks in category '{category_filter}':")
    else:
        state.logger.info("Listing all tasks:")

    # Apply filters
    filtered = []
    for todo in todos:
        # Category filter
        if category_filter and category_filter not in todo.category:
            continue
        # Priority filter
        if priority_filter and todo.priority != priority_filter:
            continue
        # Completed/pending filters
        if show_completed and not todo.completed:
            continue
        if show_pending and todo.completed:
            continue
        filtered.append(todo)

    return filtered


def _sort_todo_list(todos: list[TodoRecord]) -> list[TodoRecord] | None:
    """Sort a list of todo tasks based on priority and due date.

    Args:
        todos (list[TodoRecord]): List of todo tasks to sort.

    Returns:
        sorted (list[TodoRecord] | None): Sorted list of todo tasks or None if input list is empty.
    """
    if not todos:
        return

    sorted = todos.copy()

    sorted.sort(
        key=lambda x: (
            {"High": 1, "Med": 2, "Low": 3}.get(x.priority or "", 4),
            x.due_date or datetime.max,
        )
    )
    return sorted


def handle_list_tasks(state: TodoState, storage: TodoStorage, args: argparse.Namespace) -> None:
    """Display a list of all todo tasks.

    Args:
        state (TodoState): Current application state.
        storage (TodoStorage): Persistent storage handler.
        args (argparse.Namespace): Parsed command-line arguments.
    """
    todos = _filtered_list(state, storage, args)
    todos = _sort_todo_list(todos) if todos else None
    if not todos:
        state.logger.info("No tasks found.")
        return

    for i, todo in enumerate(todos):
        _print_todo(todo, i + 1)


def handle_mark_complete(state: TodoState, storage: TodoStorage, todo_id: str) -> None:
    """Mark a todo item as completed.

    Args:
        state (TodoState): Current application state.
        storage (TodoStorage): Persistent storage handler.
        todo_id (str): The ID of the todo to mark as complete.

    Returns:
        None
    """
    success = storage.mark_completed(todo_id)
    if success:
        state.logger.success(f"Marked task {todo_id} as completed.")
    else:
        state.logger.warn(f"Task {todo_id} not found.")


def handle_delete_task(state: TodoState, storage: TodoStorage, todo_id: str) -> None:
    """Delete a todo item from persistent storage.

    Args:
        state (TodoState): Current application state.
        storage (TodoStorage): Persistent storage handler.
        todo_id (str): The ID of the todo to delete.

    Returns:
        None
    """
    success = storage.remove_todo(todo_id)
    if success:
        state.logger.success(f"Deleted task {todo_id}.")
    else:
        state.logger.warn(f"Task {todo_id} not found.")


def _print_todo(todo: TodoRecord, i: int) -> None:
    """Print a formatted representation of a todo item.

    Args:
        todo (TodoRecord): The todo item to print.
        i (int): The index number for display.
    """
    status = "[X]" if todo.completed else "[ ]"
    cat_str = f" [{', '.join(todo.category)}]" if todo.category else ""
    due_str = f" (Due: {todo.due_date.strftime('%Y-%m-%d')})" if todo.due_date else ""

    priority_color = (
        HIGH_COLOR
        if todo.priority == "High"
        else MED_COLOR
        if todo.priority == "Med"
        else LOW_COLOR
        if todo.priority == "Low"
        else RESET_COLOR
    )

    print(
        f"{priority_color}{i}{RESET_COLOR}.{status} {todo.id}: {todo.description or '(no description)'}{cat_str}{due_str}"
    )
