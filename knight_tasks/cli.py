"""Command-line interface for knight-tasks."""
from __future__ import annotations

import argparse
import sys
from datetime import date, datetime

from . import service, storage
from .models import PRIORITIES


def _due_arg(text: str) -> date:
    try:
        return datetime.strptime(text, "%Y-%m-%d").date()
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"invalid date {text!r}, expected YYYY-MM-DD"
        ) from None


def _format_task(task) -> str:
    mark = "x" if task.done else " "
    line = f"[{mark}] #{task.id} {task.title} ({task.priority})"
    if task.due:
        line += f" due {task.due.isoformat()}"
    return line


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="knight-tasks")
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="add a task")
    add.add_argument("title")
    add.add_argument("--priority", choices=PRIORITIES, default="medium")
    add.add_argument("--due", type=_due_arg, default=None, metavar="YYYY-MM-DD")

    done = sub.add_parser("done", help="mark a task complete")
    done.add_argument("task_id", type=int)

    ls = sub.add_parser("list", help="list tasks")
    ls.add_argument("--sort", choices=("id", "priority"), default="id")
    ls.add_argument("--open-only", action="store_true")

    sub.add_parser("overdue", help="list open tasks past their due date")

    sub.add_parser("stats", help="show summary statistics")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    tasks = storage.load_tasks()

    if args.command == "add":
        task = service.add_task(tasks, args.title, args.priority, args.due)
        storage.save_tasks(tasks)
        print(f"Added #{task.id}: {task.title} [{task.priority}]"
              + (f" due {task.due.isoformat()}" if task.due else ""))
    elif args.command == "done":
        try:
            task = service.complete_task(tasks, args.task_id)
        except KeyError as exc:
            print(f"error: {exc.args[0]}", file=sys.stderr)
            return 1
        storage.save_tasks(tasks)
        print(f"Completed #{task.id}: {task.title}")
    elif args.command == "list":
        for task in service.list_tasks(
            tasks, sort_by=args.sort, include_done=not args.open_only
        ):
            print(_format_task(task))
    elif args.command == "overdue":
        late = service.overdue_tasks(tasks, date.today())
        if not late:
            print("No overdue tasks.")
        for task in late:
            print(_format_task(task))
    elif args.command == "stats":
        summary = service.stats(tasks)
        print(f"Total: {summary['total']}")
        print(f"Done:  {summary['done']}")
        print(f"Open:  {summary['open']}")
        print(f"Completion rate: {summary['completion_rate']:.0%}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
