from knight_tasks import storage
from knight_tasks.models import Task


def test_round_trip(tmp_path):
    path = tmp_path / "tasks.json"
    tasks = [Task(id=1, title="A"), Task(id=2, title="B", priority="high", done=True)]
    storage.save_tasks(tasks, path)
    assert storage.load_tasks(path) == tasks


def test_missing_file_returns_empty(tmp_path):
    assert storage.load_tasks(tmp_path / "nope.json") == []
