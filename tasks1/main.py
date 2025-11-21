# tasks1/main.py
# Simple JSON-based task manager prototype for the assignment

import json
import os
import argparse
from datetime import datetime

DATA_FILE = "tasks1_tasks.json"


def load_tasks():
    """Load tasks from the JSON file, or return empty list if none."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []


def save_tasks(tasks):
    """Save list of tasks back to the JSON file."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)


def add_task(title):
    """Add a new task with a title."""
    tasks = load_tasks()
    task = {
        "id": len(tasks) + 1,
        "title": title,
        "created": datetime.now().isoformat(timespec="seconds"),
        "status": "open",
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Added task #{task['id']}: {task['title']}")


def list_tasks():
    """List all tasks."""
    tasks = load_tasks()
    if not tasks:
        print("No tasks yet.")
        return
    for t in tasks:
        print(f"[{t['id']}] {t['title']} ({t['status']})")


def search_tasks(keyword):
    """Search tasks whose title contains the keyword."""
    tasks = load_tasks()
    keyword = keyword.lower()
    matches = [t for t in tasks if keyword in t["title"].lower()]
    if not matches:
        print("No matches.")
        return
    for t in matches:
        print(f"[{t['id']}] {t['title']} ({t['status']})")


def main():
    parser = argparse.ArgumentParser(description="tasks1 JSON task manager prototype")
    sub = parser.add_subparsers(dest="cmd")

    p_add = sub.add_parser("add", help="Add a new task")
    p_add.add_argument("title")

    sub.add_parser("list", help="List tasks")

    p_search = sub.add_parser("search", help="Search tasks by keyword")
    p_search.add_argument("keyword")

    args = parser.parse_args()

    if args.cmd == "add":
        add_task(args.title)
    elif args.cmd == "list":
        list_tasks()
    elif args.cmd == "search":
        search_tasks(args.keyword)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
