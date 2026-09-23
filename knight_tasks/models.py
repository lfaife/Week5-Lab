"""Data model for knight-tasks."""
from __future__ import annotations

from dataclasses import asdict, dataclass

PRIORITIES = ("low", "medium", "high")


@dataclass
class Task:
    id: int
    title: str
    priority: str = "medium"
    done: bool = False

    def __post_init__(self) -> None:
        if self.priority not in PRIORITIES:
            raise ValueError(
                f"priority must be one of {PRIORITIES}, got {self.priority!r}"
            )
        if not self.title.strip():
            raise ValueError("title must not be empty")

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        return cls(
            id=data["id"],
            title=data["title"],
            priority=data.get("priority", "medium"),
            done=data.get("done", False),
        )
