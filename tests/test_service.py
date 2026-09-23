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
