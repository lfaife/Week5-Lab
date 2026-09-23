"""JSON file persistence for tasks."""
from __future__ import annotations

import json
import os
from pathlib import Path

from .models import Task

DEFAULT_FILE = "tasks.json"


def storage_path() -> Path:
    return Path(os.environ.get("KNIGHT_TASKS_FILE", DEFAULT_FILE))


def load_tasks(path: Path | None = None) -> list[Task]:
    path = path or storage_path()
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as fh:
        raw = json.load(fh)
    return [Task.from_dict(item) for item in raw]


def save_tasks(tasks: list[Task], path: Path | None = None) -> None:
    path = path or storage_path()
    with path.open("w", encoding="utf-8") as fh:
        json.dump([t.to_dict() for t in tasks], fh, indent=2)
