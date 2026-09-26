import pytest

from knight_tasks import cli, storage


@pytest.fixture(autouse=True)
def tasks_file(tmp_path, monkeypatch):
    path = tmp_path / "tasks.json"
    monkeypatch.setenv("KNIGHT_TASKS_FILE", str(path))
    return path


def test_add_with_valid_due_persists(capsys):
    assert cli.main(["add", "Thing", "--due", "2030-01-15"]) == 0
    assert "due 2030-01-15" in capsys.readouterr().out
    assert storage.load_tasks()[0].due.isoformat() == "2030-01-15"


@pytest.mark.parametrize("bad", ["2026-13-01", "2026-02-30", "tomorrow", "20261001"])
def test_add_with_invalid_due_errors(bad, capsys):
    with pytest.raises(SystemExit) as exc:
        cli.main(["add", "Thing", "--due", bad])
    assert exc.value.code == 2
    assert "YYYY-MM-DD" in capsys.readouterr().err
    assert storage.load_tasks() == []


def test_list_shows_due_date_only_when_set(capsys):
    cli.main(["add", "With", "--due", "2030-01-15"])
    cli.main(["add", "Without"])
    capsys.readouterr()
    cli.main(["list"])
    lines = capsys.readouterr().out.splitlines()
    assert lines[0].endswith("due 2030-01-15")
    assert "due" not in lines[1]


def test_overdue_command_lists_only_overdue(capsys):
    cli.main(["add", "Late", "--due", "2020-01-01"])
    cli.main(["add", "Later", "--due", "2999-01-01"])
    capsys.readouterr()
    cli.main(["overdue"])
    out = capsys.readouterr().out
    assert "Late" in out and "Later" not in out
