"""Command-line interface for knight-tasks."""
from __future__ import annotations

import argparse
import sys

from . import service, storage
from .models import PRIORITIES


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="knight-tasks")
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="add a task")
    add.add_argument("title")
    add.add_argument("--priority", choices=PRIORITIES, default="medium")

    done = sub.add_parser("done", help="mark a task complete")
    done.add_argument("task_id", type=int)

    ls = sub.add_parser("list", help="list tasks")
    ls.add_argument("--sort", choices=("id", "priority"), default="id")
    ls.add_argument("--open-only", action="store_true")

    sub.add_parser("stats", help="show summary statistics")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    tasks = storage.load_tasks()

    if args.command == "add":
        task = service.add_task(tasks, args.title, args.priority)
        storage.save_tasks(tasks)
        print(f"Added #{task.id}: {task.title} [{task.priority}]")
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
            mark = "x" if task.done else " "
            print(f"[{mark}] #{task.id} {task.title} ({task.priority})")
    elif args.command == "stats":
        summary = service.stats(tasks)
        print(f"Total: {summary['total']}")
        print(f"Done:  {summary['done']}")
        print(f"Open:  {summary['open']}")
        print(f"Completion rate: {summary['completion_rate']:.0%}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
