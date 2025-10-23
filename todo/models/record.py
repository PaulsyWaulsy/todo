"""Todo data models: metadata and record definitions."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class TodoMetadata:
    """Metadata describing a Todo item.

    This class stores basic, serializable information about a Todo item.
    It does not depend on file system paths or runtime context, making it
    suitable for JSON storage, APIs, or lightweight transfers.

    Attributes:
        id (str): Unique identifier for the todo item.
        created_at (datetime): Timestamp when the todo was created.
        completed (bool): Whether the todo is marked as completed.
        category (list[str]): List of category labels or tags.
        description (Optional[str]): Optional human-readable description.
    """

    id: str
    created_at: datetime
    completed: bool = False
    category: List[str] = field(default_factory=list)
    description: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[datetime] = None

    def to_json_dict(self) -> Dict[str, Any]:
        """Convert the TodoMetadata object into a JSON-serializable dictionary.

        Returns:
            dict[str, Any]: A dictionary representation suitable for
            serialization via `json.dump`.
        """
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "completed": self.completed,
            "category": self.category,
            "description": self.description,
            "priority": self.priority,
            "due_date": self.due_date.isoformat() if self.due_date else None,
        }

    @classmethod
    def from_json_dict(cls, payload: Dict[str, Any]) -> TodoMetadata:
        """Reconstruct a TodoMetadata instance from a JSON dictionary.

        Args:
            payload (dict[str, Any]): A dictionary containing todo metadata.

        Returns:
            TodoMetadata: The reconstructed metadata object.
        """
        return cls(
            id=payload["id"],
            created_at=datetime.fromisoformat(payload["created_at"]),
            completed=payload.get("completed", False),
            category=payload.get("category", []),
            description=payload.get("description"),
        )


@dataclass
class TodoRecord(TodoMetadata):
    """A Todo item with attached file system context.

    Extends `TodoMetadata` by including information about where the record
    is stored in the local file system. This class is useful for linking
    metadata to persistent JSON files or directories.

    Attributes:
        folder (Path): Directory containing this todo record.
        data_file (Optional[Path]): Path to the todo data file (if any).
    """

    folder: Path = field(default_factory=Path)
    data_file: Optional[Path] = None
    priority: Optional[str] = None  # "Low", "Med", "High"
    due_date: Optional[datetime] = None  # stored as datetime object

    def to_json_dict(self) -> Dict[str, Any]:
        """Convert the TodoRecord object into a JSON-serializable dictionary.

        Returns:
            dict[str, Any]: Dictionary representation including file paths.
        """
        data = super().to_json_dict()
        data["folder"] = str(self.folder)
        data["priority"] = self.priority
        data["due_date"] = self.due_date.isoformat() if self.due_date else None
        if self.data_file:
            data["data_file"] = str(self.data_file)
        return data

    @classmethod
    def from_json_dict(cls, payload: Dict[str, Any], base_dir: Path) -> TodoRecord:
        """Reconstruct a TodoRecord from a JSON dictionary and base directory.

        Args:
            payload (dict[str, Any]): Dictionary containing serialized record data.
            base_dir (Path): Base directory where todo records are stored.

        Returns:
            TodoRecord: The reconstructed record with resolved folder and data file paths.
        """
        folder = base_dir / payload.get("folder", "")
        data_file = folder / "todo.json" if folder.exists() else None

        due = payload.get("due_date")
        due_date = datetime.fromisoformat(due) if due else None

        return cls(
            id=payload["id"],
            created_at=datetime.fromisoformat(payload["created_at"]),
            completed=payload.get("completed", False),
            category=payload.get("category", []),
            description=payload.get("description"),
            folder=folder,
            data_file=data_file,
            priority=payload.get("priority"),
            due_date=due_date,
        )
