"""Business logic for knight-tasks. No I/O in this module."""
from __future__ import annotations

from .models import Task


def next_id(tasks: list[Task]) -> int:
    return max((t.id for t in tasks), default=0) + 1


def add_task(tasks: list[Task], title: str, priority: str = "medium") -> Task:
    task = Task(id=next_id(tasks), title=title, priority=priority)
    tasks.append(task)
    return task


def complete_task(tasks: list[Task], task_id: int) -> Task:
    for task in tasks:
        if task.id == task_id:
            task.done = True
            return task
    raise KeyError(f"no task with id {task_id}")


def list_tasks(
    tasks: list[Task], sort_by: str = "id", include_done: bool = True
) -> list[Task]:
    visible = [t for t in tasks if include_done or not t.done]
    if sort_by == "id":
        return sorted(visible, key=lambda t: t.id)
    if sort_by == "priority":
        # Highest priority first.
        return sorted(visible, key=lambda t: t.priority)
    raise ValueError(f"unknown sort key: {sort_by!r}")


def completion_rate(tasks: list[Task]) -> float:
    """Fraction of tasks that are done, from 0.0 to 1.0."""
    done = sum(1 for t in tasks if t.done)
    return done / len(tasks)


def stats(tasks: list[Task]) -> dict:
    return {
        "total": len(tasks),
        "done": sum(1 for t in tasks if t.done),
        "open": sum(1 for t in tasks if not t.done),
        "completion_rate": completion_rate(tasks),
    }
