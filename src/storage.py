"""Storage module for the Todo application."""

from __future__ import annotations

import json
from pathlib import Path
from typing import List, Optional
from datetime import datetime

# Locals import
from .record import TodoRecord


class TodoStorage:
    """Manages persistence of Todo records on disk.

    Handles reading and writing todo records to a JSON file, including
    serialization, deserialization, and simple ID management.

    Attributes:
        root (Path): Root directory for todo data storage.
        filepath (Path): Full path to the JSON file storing todos.
    """

    def __init__(self, root: Path, filename: str = "todo.json") -> None:
        """Initialize a TodoStorage instance.

        Args:
            root (Path): Directory to store the todo data file.
            filename (str): JSON filename for todos. Defaults to "todo.json".
        """
        self.root = root
        self.filepath = self._ensure_todo_file(filename)

    def _ensure_todo_file(self, filename: str) -> Path:
        """Ensure that the todo storage file exists.

        Args:
            filename (str): Name of the JSON file.

        Returns:
            Path: Absolute path to the storage file.
        """
        self.root.mkdir(parents=True, exist_ok=True)
        path = self.root / filename
        if not path.exists():
            path.write_text("[]", encoding="utf-8")
        return path

    def load_todos(self) -> List[TodoRecord]:
        """Load all todos from disk into TodoRecord objects.

        Returns:
            list[TodoRecord]: A list of deserialized todo records.
        """
        if not self.filepath.exists():
            return []

        with open(self.filepath, "r", encoding="utf-8") as file:
            data = json.load(file)

        todos = [TodoRecord.from_json_dict(item, base_dir=self.root) for item in data]
        return todos

    def save_todos(self, todos: List[TodoRecord]) -> None:
        """Write all todos to disk as JSON.

        Args:
            todos (list[TodoRecord]): List of todos to serialize and store.
        """
        data = [todo.to_json_dict() for todo in todos]
        with open(self.filepath, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

    def add_todo(self, todo: TodoRecord) -> None:
        """Add a new todo to storage and persist it.

        Args:
            todo (TodoRecord): The todo record to add.
        """
        todos = self.load_todos()
        todos.append(todo)
        self.save_todos(todos)

    def remove_todo(self, todo_id: str) -> bool:
        """Remove a todo from storage by ID.

        Args:
            todo_id (str): Unique ID of the todo to remove.

        Returns:
            bool: True if the todo was removed, False if not found.
        """
        todos = self.load_todos()
        filtered = [t for t in todos if t.id != todo_id]
        if len(filtered) == len(todos):
            return False
        self.save_todos(filtered)
        return True

    def get_todo(self, todo_id: str) -> Optional[TodoRecord]:
        """Retrieve a specific todo by ID.

        Args:
            todo_id (str): Unique ID of the todo.

        Returns:
            TodoRecord | None: The found todo, or None if not found.
        """
        todos = self.load_todos()
        for todo in todos:
            if todo.id == todo_id:
                return todo
        return None

    def mark_completed(self, todo_id: str) -> bool:
        """Mark a todo as completed and update storage.

        Args:
            todo_id (str): Unique ID of the todo.

        Returns:
            bool: True if update succeeded, False otherwise.
        """
        todos = self.load_todos()
        for todo in todos:
            if todo.id == todo_id:
                todo.completed = True
                self.save_todos(todos)
                return True
        return False


def generate_todo_id(prefix: str = "todo") -> str:
    """Generate a timestamp-based todo ID.

    Args:
        prefix (str): Optional ID prefix. Defaults to "todo".

    Returns:
        str: Unique identifier string.
    """
    now = datetime.now()
    return f"{prefix}_{now.strftime('%Y%m%d_%H%M%S')}"
