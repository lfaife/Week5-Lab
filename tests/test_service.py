import pytest

from knight_tasks import service
from knight_tasks.models import Task


def make_tasks():
    return [
        Task(id=1, title="Read chapter 4", priority="low"),
        Task(id=2, title="Submit lab", priority="high", done=True),
        Task(id=3, title="Email TA", priority="medium"),
    ]


def test_add_task_assigns_next_id():
    tasks = make_tasks()
    task = service.add_task(tasks, "New thing")
    assert task.id == 4
    assert task in tasks


def test_complete_task_marks_done():
    tasks = make_tasks()
    service.complete_task(tasks, 1)
    assert tasks[0].done is True


def test_complete_task_unknown_id_raises():
    with pytest.raises(KeyError):
        service.complete_task(make_tasks(), 99)


def test_list_open_only_hides_done():
    result = service.list_tasks(make_tasks(), include_done=False)
    assert [t.id for t in result] == [1, 3]


def test_completion_rate():
    assert service.completion_rate(make_tasks()) == pytest.approx(1 / 3)


def test_stats_on_empty_list():
    # A brand-new user has no tasks. `stats` must not crash.
    assert service.stats([]) == {
        "total": 0,
        "done": 0,
        "open": 0,
        "completion_rate": 0.0,
    }


def test_add_task_with_due_date():
    from datetime import date

    task = service.add_task([], "Due thing", due=date(2026, 10, 1))
    assert task.due == date(2026, 10, 1)


def test_overdue_returns_open_past_due_only():
    from datetime import date

    today = date(2026, 9, 26)
    tasks = [
        Task(id=1, title="late", due=date(2026, 9, 1)),
        Task(id=2, title="future", due=date(2026, 12, 1)),
        Task(id=3, title="no due"),
        Task(id=4, title="late but done", due=date(2026, 9, 1), done=True),
    ]
    assert [t.id for t in service.overdue_tasks(tasks, today)] == [1]


def test_overdue_excludes_task_due_today():
    from datetime import date

    today = date(2026, 9, 26)
    assert service.overdue_tasks([Task(id=1, title="t", due=today)], today) == []


def test_overdue_sorted_by_due_date():
    from datetime import date

    tasks = [
        Task(id=1, title="b", due=date(2026, 9, 10)),
        Task(id=2, title="a", due=date(2026, 9, 1)),
    ]
    result = service.overdue_tasks(tasks, date(2026, 9, 26))
    assert [t.id for t in result] == [2, 1]
