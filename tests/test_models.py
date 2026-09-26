from datetime import date

from knight_tasks.models import Task


def test_task_dict_round_trip_with_and_without_due():
    for task in (Task(id=1, title="A"), Task(id=2, title="B", due=date(2026, 1, 2))):
        assert Task.from_dict(task.to_dict()) == task


def test_from_dict_missing_due_defaults_to_none():
    assert Task.from_dict({"id": 1, "title": "Old"}).due is None
