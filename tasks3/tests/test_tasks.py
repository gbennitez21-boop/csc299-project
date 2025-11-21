import sys
import pathlib

# Add the root of tasks3 (where main.py lives) to Python path
ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from main import add_task, list_tasks


def test_add_task_creates_entry(tmp_path, monkeypatch):
    # Redirect the data file into a temp directory
    test_file = tmp_path / "tasks3_tasks.json"
    monkeypatch.setattr("main.DATA_FILE", str(test_file))

    add_task("Study for exam", due="2025-12-01", tags=["school"])

    tasks = list_tasks()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Study for exam"
    assert tasks[0]["due"] == "2025-12-01"
    assert "school" in tasks[0]["tags"]
