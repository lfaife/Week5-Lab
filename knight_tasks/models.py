"""Data model for knight-tasks."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date

PRIORITIES = ("low", "medium", "high")


@dataclass
class Task:
    id: int
    title: str
    priority: str = "medium"
    done: bool = False
    due: date | None = None

    def __post_init__(self) -> None:
        if self.priority not in PRIORITIES:
            raise ValueError(
                f"priority must be one of {PRIORITIES}, got {self.priority!r}"
            )
        if not self.title.strip():
            raise ValueError("title must not be empty")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "priority": self.priority,
            "done": self.done,
            "due": self.due.isoformat() if self.due else None,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        return cls(
            id=data["id"],
            title=data["title"],
            priority=data.get("priority", "medium"),
            done=data.get("done", False),
            due=date.fromisoformat(data["due"]) if data.get("due") else None,
        )
