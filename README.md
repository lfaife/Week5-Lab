# knight-tasks

A small command-line task tracker used in the Week 1 agentic AI hands-on.

## Setup

    python -m venv .venv
    source .venv/bin/activate        # Windows: .venv\Scripts\activate
    pip install -r requirements.txt

## Run

    python -m knight_tasks.cli add "Write lab report" --priority high
    python -m knight_tasks.cli list
    python -m knight_tasks.cli done 1
    python -m knight_tasks.cli stats

Tasks are stored in `tasks.json` in the current directory
(override with the `KNIGHT_TASKS_FILE` environment variable).

## Test

    python -m pytest -q

One test fails on purpose. Do not fix it by hand; that is the agent's job in class.
