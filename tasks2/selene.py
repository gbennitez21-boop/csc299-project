# tasks2/selene.py — Selene: Self-Knowledge System (JSON-based, single-file app)
# Python 3.10+

import argparse
import json
import os
from datetime import datetime, timedelta
from collections import Counter

DATA_FILE = "selene_data.json"


# -----------------------------
# Storage
# -----------------------------
def _now():
    return datetime.now().isoformat(timespec="seconds")


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
    else:
        data = {}
    # default structure
    data.setdefault("tasks", [])
    data.setdefault("notes", [])
    data.setdefault("cycle_logs", [])  # entries: {"date":"YYYY-MM-DD","phase":"start|end|note","symptoms":[],"mood":""}
    data.setdefault("config", {"avg_cycle_length": 28})
    return data


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


# -----------------------------
# Helpers
# -----------------------------
def parse_date(s: str | None):
    if not s:
        return None
    try:
        return datetime.fromisoformat(s).date()
    except ValueError:
        # allow YYYY-MM-DD only
        try:
            return datetime.strptime(s, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Invalid date. Use YYYY-MM-DD.")


def next_id(seq):
    return (max((item["id"] for item in seq), default=0) + 1) if seq else 1


def fmt_date(d):
    return d if isinstance(d, str) else (d.isoformat() if d else "—")


# -----------------------------
# Tasks
# -----------------------------
def task_add(args):
    data = load_data()
    t = {
        "id": next_id(data["tasks"]),
        "title": args.title,
        "due": args.due if args.due else None,
        "tags": args.tags or [],
        "energy": (args.energy or "").lower() or None,  # high|low|creative|reflective
        "status": "open",
        "created": _now(),
        "updated": _now(),
    }
    data["tasks"].append(t)
    save_data(data)
    print(f"✨ Added task [{t['id']}] {t['title']}")


def task_list(args):
    data = load_data()
    tasks = data["tasks"]
    status = args.status
    if status != "all":
        tasks = [t for t in tasks if t["status"] == status]
    # sort
    if args.sort == "due":
        def k(t):
            return (t["due"] or "9999-12-31", t.get("energy") or "", t["title"])
    elif args.sort == "updated":
        def k(t):
            return t["updated"]
    else:
        def k(t):
            return t["title"]
    tasks = sorted(tasks, key=k)
    if not tasks:
        print("(no tasks)")
        return
    for t in tasks:
        icon = "✅" if t["status"] == "done" else "🕓"
        due = t["due"] or "—"
        energy = t.get("energy") or "—"
        tags = ", ".join(t.get("tags", [])) or "—"
        print(f"[{t['id']}] {icon} {t['title']} | due: {due} | energy: {energy} | tags: {tags}")


def task_done(args):
    data = load_data()
    for t in data["tasks"]:
        if t["id"] == args.id:
            t["status"] = "done"
            t["updated"] = _now()
            save_data(data)
            print(f"🎯 Task {args.id} marked done.")
            return
    print("❌ Task not found.")


def task_delete(args):
    data = load_data()
    before = len(data["tasks"])
    data["tasks"] = [t for t in data["tasks"] if t["id"] != args.id]
    after = len(data["tasks"])
    save_data(data)
    if after < before:
        print(f"🗑️ Deleted task {args.id}.")
    else:
        print("❌ Task not found.")


def task_search(args):
    data = load_data()
    q = args.keyword.lower()
    matches = [t for t in data["tasks"] if q in t["title"].lower()]
    if not matches:
        print("(no matches)")
        return
    for t in matches:
        print(f"[{t['id']}] {t['title']} | status: {t['status']} | due: {t['due'] or '—'}")


# -----------------------------
# Notes (PKMS basics)
# -----------------------------
def note_add(args):
    data = load_data()
    n = {
        "id": next_id(data["notes"]),
        "title": args.title,
        "body": args.body or "",
        "tags": args.tags or [],
        "created": _now(),
        "updated": _now(),
    }
    data["notes"].append(n)
    save_data(data)
    print(f"📝 Added note [{n['id']}] {n['title']}")


def note_list(args):
    data = load_data()
    notes = data["notes"]
    if args.tag:
        notes = [n for n in notes if args.tag in n.get("tags", [])]
    notes = sorted(notes, key=lambda n: n["updated"], reverse=True)
    if not notes:
        print("(no notes)")
        return
    for n in notes[: args.limit]:
        tags = ", ".join(n.get("tags", [])) or "—"
        print(f"[{n['id']}] {n['title']} | tags: {tags} | updated: {n['updated']}")


def note_show(args):
    data = load_data()
    for n in data["notes"]:
        if n["id"] == args.id:
            tags = ", ".join(n.get("tags", [])) or "—"
            print(f"# {n['title']}\n")
            if tags != "—":
                print(f"tags: {tags}\n")
            print(n.get("body", ""))
            return
    print("❌ Note not found.")


def note_search(args):
    data = load_data()
    q = args.keyword.lower()
    matches = [n for n in data["notes"] if q in n["title"].lower() or q in n.get("body", "").lower()]
    if not matches:
        print("(no matches)")
        return
    for n in matches:
        print(f"[{n['id']}] {n['title']}")


# -----------------------------
# Cycle tracking
# -----------------------------
def cycle_log(args):
    data = load_data()
    date = parse_date(args.date).isoformat()
    entry = {
        "date": date,
        "phase": args.phase,  # start|end|note
        "symptoms": args.symptoms or [],
        "mood": args.mood or "",
        "note": args.note or "",
        "created": _now(),
    }
    data["cycle_logs"].append(entry)
    # keep sorted by date
    data["cycle_logs"] = sorted(data["cycle_logs"], key=lambda e: e["date"])
    save_data(data)
    print(f"🩸 Logged {entry['phase']} on {entry['date']}")


def cycle_show(args):
    data = load_data()
    logs = data["cycle_logs"]
    if not logs:
        print("(no cycle logs)")
        return
    # show last N
    logs = logs[-args.last :]
    for e in logs:
        sym = ", ".join(e.get("symptoms", [])) or "—"
        mood = e.get("mood") or "—"
        note = e.get("note") or ""
        print(f"{e['date']} | {e['phase']} | mood: {mood} | symptoms: {sym} {('| ' + note) if note else ''}")


def _recent_starts(logs, max_count=6):
    starts = [parse_date(e["date"]) for e in logs if e.get("phase") == "start"]
    starts = sorted(d for d in starts if d is not None)
    return starts[-max_count:]


def cycle_predict(args):
    data = load_data()
    logs = data["cycle_logs"]
    starts = _recent_starts(logs)
    if not starts:
        avg = data["config"]["avg_cycle_length"]
        print(f"No start logs yet. Using avg length {avg} days: next start unknown until first log.")
        return
    # compute average from diffs if we have 2+
    diffs = []
    for i in range(1, len(starts)):
        diffs.append((starts[i] - starts[i - 1]).days)
    if diffs:
        avg = round(sum(diffs) / len(diffs))
    else:
        avg = data["config"]["avg_cycle_length"]
    next_start = starts[-1] + timedelta(days=avg)
    print(f"Predicted next start: {next_start.isoformat()} (avg {avg} days from {len(diffs) or 1} cycle(s))")


def cycle_stats(args):
    data = load_data()
    logs = data["cycle_logs"]
    if not logs:
        print("(no cycle logs)")
        return
    starts = _recent_starts(logs, max_count=12)
    diffs = [(starts[i] - starts[i - 1]).days for i in range(1, len(starts))]
    avg = round(sum(diffs) / len(diffs)) if diffs else data["config"]["avg_cycle_length"]
    # symptom frequency
    symptoms = []
    for e in logs:
        symptoms.extend(e.get("symptoms", []))
    cnt = Counter(symptoms)
    top = ", ".join(f"{k}×{v}" for k, v in cnt.most_common(5)) or "—"
    print(f"Average cycle length: {avg} days")
    print(f"Logged starts considered: {len(starts)}")
    print(f"Common symptoms: {top}")


# -----------------------------
# Plan & Chat (local heuristic)
# -----------------------------
LOW_ENERGY_HINTS = [
    "journaling", "reading", "planning", "research", "refactoring", "clean up notes"
]
HIGH_ENERGY_HINTS = [
    "deep work", "coding sprint", "meetings", "outreach", "presentations"
]


def _current_phase_hint(data):
    # crude heuristic: if within 2 days of a 'start', assume low energy window
    logs = data["cycle_logs"]
    starts = _recent_starts(logs)
    today = datetime.now().date()
    if starts:
        last_start = starts[-1]
        delta = (today - last_start).days
        if 0 <= delta <= 2:
            return "low"
    return "normal"


def plan(args):
    data = load_data()
    tasks = [t for t in data["tasks"] if t["status"] == "open"]
    if not tasks:
        print("(no open tasks)")
        return

    phase = _current_phase_hint(data)
    if phase == "low":
        preferred = {"low", "reflective", None, ""}
        msg = "You’re near a low-energy window. Favor gentle focus."
        hints = LOW_ENERGY_HINTS
    else:
        preferred = {"high", "creative", None, ""}
        msg = "Normal/high energy window. Go bold."
        hints = HIGH_ENERGY_HINTS

    # prioritize by energy tag match, then due date
    def score(t):
        energy = (t.get("energy") or "").lower() or None
        match = 0 if energy in preferred else 1
        due = t.get("due") or "9999-12-31"
        return (match, due, t["title"])

    ranked = sorted(tasks, key=score)
    print(msg)
    for t in ranked[:10]:
        due = t.get("due") or "—"
        en = t.get("energy") or "—"
        print(f"- [{t['id']}] {t['title']} (due {due}, energy {en})")
    print(f"\nSuggestions: {', '.join(hints)}")


def chat(args):
    """Local, simple retrieval over notes/tasks."""
    data = load_data()
    q = " ".join(args.query).lower()

    # retrieve notes
    notes = [n for n in data["notes"] if q in n["title"].lower() or q in n.get("body", "").lower()]
    # retrieve tasks
    tasks = [t for t in data["tasks"] if q in t["title"].lower()]

    if not notes and not tasks:
        print("I don’t see anything on that yet. Try adding a note or task first.")
        return

    print("Here’s what I found:")
    for n in notes[:5]:
        preview = (n.get("body", "") or "").strip().replace("\n", " ")
        if len(preview) > 100:
            preview = preview[:100] + "…"
        print(f"• Note#{n['id']}: {n['title']} — {preview}")
    for t in tasks[:5]:
        due = t.get("due") or "—"
        print(f"• Task#{t['id']}: {t['title']} (due {due})")


# -----------------------------
# Export
# -----------------------------
def export_json(args):
    data = load_data()
    path = args.path or "selene_export.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"📦 Exported to {path}")


# -----------------------------
# CLI wiring
# -----------------------------
def build_parser():
    p = argparse.ArgumentParser(
        description="Selene — Self-Knowledge System (tasks, notes, cycle tracking, JSON storage)"
    )
    sub = p.add_subparsers(dest="cmd")

    # tasks
    sp = sub.add_parser("task-add", help="Add a task")
    sp.add_argument("title")
    sp.add_argument("--due")
    sp.add_argument("--tags", nargs="*")
    sp.add_argument("--energy", choices=["high", "low", "creative", "reflective"])
    sp.set_defaults(func=task_add)

    sp = sub.add_parser("task-list", help="List tasks")
    sp.add_argument("--status", default="open", choices=["open", "done", "all"])
    sp.add_argument("--sort", default="due", choices=["due", "title", "updated"])
    sp.set_defaults(func=task_list)

    sp = sub.add_parser("task-done", help="Mark task done")
    sp.add_argument("id", type=int)
    sp.set_defaults(func=task_done)

    sp = sub.add_parser("task-del", help="Delete task")
    sp.add_argument("id", type=int)
    sp.set_defaults(func=task_delete)

    sp = sub.add_parser("task-search", help="Search tasks")
    sp.add_argument("keyword")
    sp.set_defaults(func=task_search)

    # notes
    sp = sub.add_parser("note-add", help="Add a note")
    sp.add_argument("title")
    sp.add_argument("--tags", nargs="*")
    sp.add_argument("--body")
    sp.set_defaults(func=note_add)

    sp = sub.add_parser("note-list", help="List notes")
    sp.add_argument("--tag")
    sp.add_argument("--limit", type=int, default=20)
    sp.set_defaults(func=note_list)

    sp = sub.add_parser("note-show", help="Show a note")
    sp.add_argument("id", type=int)
    sp.set_defaults(func=note_show)

    sp = sub.add_parser("note-search", help="Search notes")
    sp.add_argument("keyword")
    sp.set_defaults(func=note_search)

    # cycle
    sp = sub.add_parser("cycle-log", help="Log cycle info")
    sp.add_argument("date", help="YYYY-MM-DD")
    sp.add_argument("--phase", choices=["start", "end", "note"], required=True)
    sp.add_argument("--symptoms", nargs="*")
    sp.add_argument("--mood")
    sp.add_argument("--note")
    sp.set_defaults(func=cycle_log)

    sp = sub.add_parser("cycle-show", help="Show recent cycle logs")
    sp.add_argument("--last", type=int, default=10)
    sp.set_defaults(func=cycle_show)

    sp = sub.add_parser("cycle-predict", help="Predict next start date")
    sp.set_defaults(func=cycle_predict)

    sp = sub.add_parser("cycle-stats", help="Cycle stats")
    sp.set_defaults(func=cycle_stats)

    # plan & chat
    sp = sub.add_parser("plan", help="Suggest tasks based on energy window")
    sp.set_defaults(func=plan)

    sp = sub.add_parser("chat", help="Search-like chat")
    sp.add_argument("query", nargs=argparse.REMAINDER, help='Your question, e.g., chat what did I write about cramps')
    sp.set_defaults(func=chat)

    # export
    sp = sub.add_parser("export", help="Export all data to JSON")
    sp.add_argument("--path")
    sp.set_defaults(func=export_json)

    return p


def main():
    parser = build_parser()
    args = parser.parse_args()
    if not getattr(args, "cmd", None):
        parser.print_help()
        return
    try:
        args.func(args)
    except ValueError as e:
        print(f"❌ {e}")


if __name__ == "__main__":
    main()
