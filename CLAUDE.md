# CLAUDE.md


This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Architecture

**knight-tasks** is a lightweight CLI task tracker with clean separation of concerns:

- **models.py** — Data model. The `Task` dataclass (id, title, priority, done) is the core entity. Validates priorities ("low", "medium", "high") and non-empty titles in `__post_init__`.

- **service.py** — Pure business logic with no I/O. Contains `add_task()`, `complete_task()`, `list_tasks()`, `completion_rate()`, and `stats()`. This is where the application's core rules live.

- **storage.py** — JSON file persistence. Loads/saves tasks to `tasks.json` (configurable via `KNIGHT_TASKS_FILE` env var). The only module that does file I/O.

- **cli.py** — Command-line interface. Uses argparse to define subcommands (add, list, done, stats). Orchestrates calls to storage and service layers.

The flow is: **CLI → Storage (load) → Service (compute) → Storage (save) → CLI (print)**.

## Key Conventions

- Business logic lives in `service.py` and does no I/O (filesystem, network, etc.). This keeps logic testable without mocking.
- Every bug fix ships with a regression test (documented in NOTES.md).
- Tasks are stored in JSON; the storage layer handles serialization via `Task.to_dict()` and `Task.from_dict()`.

## Test Suite

Tests are in `tests/` with two files:

- **test_service.py** — 6 tests for service logic. Includes `test_stats_on_empty_list`, which intentionally fails due to a division-by-zero bug in `completion_rate()`. This is by design; the failing test is part of the lab exercise.

- **test_storage.py** — 2 tests for JSON round-tripping and missing file handling.

Note: `cli.py` has no tests (open item in NOTES.md).

## Known Issues

- `completion_rate()` in service.py crashes with `ZeroDivisionError` when the task list is empty. The `test_stats_on_empty_list` test catches this intentionally.
- `list --sort priority` may not sort correctly (unconfirmed; see NOTES.md).
- CLI layer is untested.

## Rules
- Run tests with: python -m pytest -q
- Business logic goes in knight_tasks/service.py and does no I/O.
- Every bug fix ships with a regression test.
- Never modify or delete existing tests to make them pass.
- Never read, print, or commit .env.
- Do not add third-party dependencies without asking first.
