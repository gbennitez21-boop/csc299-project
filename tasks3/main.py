import argparse
import json
import os
from datetime import datetime

DATA_FILE = "tasks3_tasks.json"


# --- required by assignment test example ---
def inc(n: int) -> int:
    return n + 1


# --- task storage helpers ---
def load_tasks():
    """Load tasks from JSON file or return empty list."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []


def save_tasks(tasks):
    """Save list of tasks back into JSON file."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)


# --- task operations ---
def add_task(title: str, due: str | None = None, tags: list[str] | None = None) -> dict:
    """Add a new task dict and persist it."""
    tasks = load_tasks()
    task = {
        "id": len(tasks) + 1,
        "title": title,
        "due": due,
        "tags": tags or [],
        "created": datetime.now().isoformat(timespec="seconds"),
        "status": "open",
    }
    tasks.append(task)
    save_tasks(tasks)
    return task


def list_tasks():
    """Return all tasks."""
    return load_tasks()


# --- CLI wiring ---
def _build_parser():
    parser = argparse.ArgumentParser(
        description="tasks3 — JSON task manager + inc() demo"
    )
    sub = parser.add_subparsers(dest="cmd")

    # task add
    p_add = sub.add_parser("add", help="Add a new task")
    p_add.add_argument("title")
    p_add.add_argument("--due")
    p_add.add_argument("--tags", nargs="*")

    # task list
    sub.add_parser("list", help="List tasks")

    # demo inc
    p_inc = sub.add_parser("inc", help="Demo inc() function")
    p_inc.add_argument("n", type=int)

    return parser


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    if args.cmd == "add":
        task = add_task(args.title, args.due, args.tags)
        print(f"Added task #{task['id']}: {task['title']}")
    elif args.cmd == "list":
        tasks = list_tasks()
        if not tasks:
            print("No tasks yet.")
        else:
            for t in tasks:
                due = t.get("due") or "—"
                tags = ", ".join(t.get("tags", [])) or "—"
                print(f"[{t['id']}] {t['title']} | due: {due} | tags: {tags} | status: {t['status']}")
    elif args.cmd == "inc":
        print(inc(args.n))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
